from importlib_resources import files
import streamlit as st
from rag_pipeline.ingestion import ingestion_pipeline, load_uploaded_pdfs, clean_text, split_doc
from intelligence.comparator import compare_documents
from intelligence.router import route_query
from intelligence.summarizer import summarize_document
from intelligence.question_solver import question_solver_document
from llm.query_rewriter import rewrite_query
# from intelligence.researcher import research_documents
from rag_pipeline.retrieval import retriever_pipeline
from src.ui.layout import layout
from src.database.db import conversations, find_conversations, store_messages, get_conversation_messages, store_uploaded_files, get_file_hash, get_documents
from io import BytesIO
from src.database.db_config import supabase

def dashboard():
    user_data= st.session_state.user_data
    
    if "button" not in st.session_state:
        st.session_state.button= None

    if "messages" not in st.session_state:
        st.session_state.messages= []

    if "new_conv_id" not in st.session_state:
        st.session_state.new_conv_id= None

    if "mode" not in st.session_state:
        st.session_state.mode= None

    if "answer" not in st.session_state:
        st.session_state.answer= None

    if "chat_version" not in st.session_state:
        st.session_state.chat_version= 0

    if "selected_docs" not in st.session_state:
        st.session_state.selected_docs= []
    
    #st.session_state.conversation= conversations(user_data['id'], title)
    layout()
    
    with st.sidebar:
        st.markdown(
            """
            <div class="main-title">
               📔 DocuMind AI
            </div>

            <div class="sub-title">
                Document Intelligence & Research
            </div>
            
            """,
            unsafe_allow_html= True
        )
        
        uploader_files= st.file_uploader(
            "Upload PDF documents",
            type= ["pdf"],
            accept_multiple_files= True,
            label_visibility= "collapsed"
        )
        total_files=0
        if uploader_files:
            print(uploader_files)
            if st.button("+ Process Document", width= "stretch"):
                
                with st.spinner("Processing document..."):
                    new_files= []
                    for file in uploader_files:
                        if not file.name.lower().endswith(".pdf"):
                            st.session_state.documents= None
                            st.warning("All files should be in pdf form.")

                        else:
                            file_bytes= file.getvalue()
                            file_hash= get_file_hash(file_bytes)

                            is_new= store_uploaded_files(file.name, user_data['id'], file_bytes, file_hash)
                            if not is_new or is_new== "file_exist":
                                st.warning(f"{file.name} already exists- skipping")
                                continue
                            new_files.append(file)

                    # st.session_state.documents= new_files
                    if new_files:
                        ingestion_pipeline(new_files)
                        st.success(f"Processed {len(new_files)} new documents")
                    else:
                        st.info('No new documents to process')
                     
        documents= get_documents(user_data['id'])
        print(documents)
        st.session_state.documents_name= [
            document['filename'] for document in documents
        ]

        if "documents_name" in st.session_state and st.session_state.documents_name: 
            st.subheader("Select files for comparison and summarization")   
            st.markdown(
                """
                <div class="sidebar-heading">
                    📑 Document Library
                </div>
                
                """,
                unsafe_allow_html= True
            )
                        
            for document in st.session_state.documents_name:
                is_checked= st.checkbox(
                    f"📄 {document}",
                    key= f"check_{document}"
                )

                if is_checked and document not in st.session_state.selected_docs:
                    st.session_state.selected_docs.append(document)
                    st.session_state.answer= None
                    st.session_state.chat_version+= 1

                if not is_checked and document in st.session_state.selected_docs:
                    st.session_state.selected_docs.remove(document)
                    st.session_state.answer= None
                    st.session_state.chat_version+= 1

                if st.session_state.selected_docs and len(st.session_state.selected_docs):
                    selected_paths= []
                    for doc in documents:
                        if doc['filename'] in st.session_state.selected_docs:
                            selected_paths.append(doc['storage_path'])

                    files_to_pass=[]
                    for path in selected_paths:
                        file_bytes= supabase.storage.from_("documents").download(path)
                        f= BytesIO(file_bytes)
                        f.name= path.split("/")[-1]
                        files_to_pass.append(f)
                total_files+=1

            st.markdown(
                f"""
                <div class="chat-heading">
                    💬 Your Chats
                </div>
                """,
                unsafe_allow_html= True
            )
            if st.button("+ New Chat", use_container_width= True):
                st.session_state.new_conv_id= None
                st.session_state.conv_title= None
                st.session_state.messages= []
                st.session_state.answer= None
                st.session_state.chat_version+= 1
                st.rerun()

            st.sidebar.divider()
            user_id= user_data['id']
            all_convos= find_conversations(user_id)

            if len(all_convos) ==0:
                st.info('start a new chat by typing in the input field.')
            else: 
                with st.container(key="chathistory-box"):
                    for convo in all_convos:
                        convo_id= convo['id']
                        convo_title= convo['title']

                        if st.button(f"💬 {convo_title}",
                            key= f"chat_btn_{convo_id}",
                            use_container_width= True,
                        ):
                            st.session_state.new_conv_id= convo_id
                            print("new convo id =", convo_id)
                            st.session_state.conv_title= convo_title
                            st.session_state.chat_version+= 1
                            st.session_state.answer= None
                            # rewritten_query= rewrite_query(query, st.session_state.messages)
                            # store_messages(convo_id, rewritten_query)
                            msgs= get_conversation_messages(convo_id)
                            st.session_state.messages= msgs[0]['content']
                            print("messages= ", st.session_state.messages)
                            st.rerun()

        else: 
            st.warning('Please upload any document')

        col1, col2, col3= st.columns([3,3,3])
        with col2:
            if st.button("Logout ->", use_container_width= True):
                st.session_state.user_login_type= "login"
                st.session_state.clear()
                st.session_state.user_data= None
                st.rerun()

    with st.container(key="right-panel"):
        st.markdown(
            """
            <div class="main-heading">
                AI Document Intelligence
            </div>

            <div class="sub-heading">
                Research Assistant
            </div>

            <div class="para">
                Ask questions, analyse doccuments, compare research, and discover insights from your document library.
            </div>

            """,
            unsafe_allow_html= True
        )
        col1, col2= st.columns(2)

        with col1:
            query= st.text_input("query", key= f"query_input_{st.session_state.chat_version}", placeholder= "e.g. What are the main limitations of the proposed method?", label_visibility= "collapsed")

        with col2:
            if st.button("Search", width="stretch"):
                st.session_state.button= "active"
            # else:
            #     st.session_state.button= None
        
        if st.session_state.button == "active":
            if not query:
                st.error("Please enter your query.")
                st.session_state.button= None
                st.rerun()

            with st.spinner("processing query..."):
                if st.session_state.new_conv_id is None:
                    title= query[:50]
                    new_conv= conversations(user_data['id'], title)
                    print("new convo id= ", new_conv)
                    st.session_state.new_conv_id= new_conv[0]['id']
                    st.session_state.conv_title= new_conv[0]['title']
                    store_messages(new_conv[0]['id'], query)
                    st.session_state.messages= get_conversation_messages(new_conv[0]['id']) 

                else:
                    print("old messages= ", st.session_state.messages)
                    if st.session_state.messages:
                        query= rewrite_query(query, st.session_state.messages)
                    print("rewritten query= ", query)
                    convo_id= st.session_state.new_conv_id
                    store_messages(convo_id, query)
                    st.session_state.messages= get_conversation_messages(convo_id)
                    print(st.session_state.messages)

                mode= route_query(query)
                st.session_state.mode= mode

        col1, col2, col3= st.columns(3)
        with col1:  
                
            st.markdown(
                """
                <div class="mode-card">
                    <div class="mode-icon">💬</div>
                    <div class="mode-name">Ask</div>
                    <div class="mode-description>
                        Ask question about your documents.
                    </div>
                </div>
                """,
                unsafe_allow_html= True
            )
                
        with col2:
            
            st.markdown(
                """
                <div class="mode-card">
                    <div class="mode-icon">📋</div>
                    <div class="mode-name">Summarize</div>
                    <div class="mode-description>
                        Generate concise document summaries.
                    </div>
                </div>
                """,
                unsafe_allow_html= True
            )
        
        with col3: 
            
            st.markdown(
                """
                <div class="mode-card">
                    <div class="mode-icon">⚖</div>
                    <div class="mode-name">Compare</div>
                    <div class="mode-description>
                        Compare documents and findings.
                    </div>
                </div>
                """,
                unsafe_allow_html= True
            )
                
        st.markdown(
            f"""
            <div class="active-mode">
                Active mode
                <span class="mode">
                    {st.session_state.mode}
                </span>
            </div>
            """,
            unsafe_allow_html= True
        )

        if st.session_state.button=="active" and query:
            with st.spinner("Processing query..."):

                if st.session_state.mode == "COMPARISON":
                    
                    if len(st.session_state.selected_docs) == 2:
                        uploaded_files= load_uploaded_pdfs(files_to_pass)
                        clean_uploaded_files= clean_text(uploaded_files)
                        all_chunks= split_doc(clean_uploaded_files)
                        document_a_chunks= get_document_chunks(all_chunks, st.session_state.documents_name[0])
                        document_b_chunks= get_document_chunks(all_chunks, st.session_state.documents_name[1])
                        answer= compare_documents(document_a_chunks, document_b_chunks)
                        st.session_state.answer= answer
                        # answer_portion()
                        
                    else:
                        st.error("Sorry! You can upload ony two files for comparison")
                    
                elif st.session_state.mode == "SUMMARY":
                    uploaded_files= load_uploaded_pdfs(files_to_pass)
                    clean_uploaded_files= clean_text(uploaded_files)
                    docs_chunks= split_doc(clean_uploaded_files)
                    answer= summarize_document(docs_chunks)
                    st.session_state.answer= answer

                elif st.session_state.mode == "QUESTION":
                    results= retriever_pipeline(query)
                    # results= retriever_obj.retrieve(query)
                    print("retrieved chunks= ", results)
                    answer, sources= question_solver_document(results, query)
                    st.session_state.answer= answer
                    st.session_state.sources= sources
                    
                else:
                    st.error("Please enter correct query.")
            st.session_state.button= None
            st.rerun()

        if st.session_state.get("answer"):
            answer_portion()

def answer_portion():
    
    st.markdown(
        """
        <div class= "section-header">
            <div class= "section-icon">🤖</div>
            <div class= "section-title"> AI Response</div>
        </div>
        """, unsafe_allow_html= True
    )

    st.markdown(
        f"""
        <div class="response-card">
            <div class="response-label">
                Generated Response
            </div>
            {st.session_state.answer}
        </div>
        """,
        unsafe_allow_html= True
    )

    st.markdown(
        """
        <div class= "section-header">
            <div class= "section-icon">📗</div>
            <div class= "section-title">Sources</div>
        </div>
        """,
        unsafe_allow_html= True
    ) 
    
    source_columns= st.columns(3)
    if st.session_state.mode== "COMPARISON" or st.session_state.mode== "SUMMARY":
        for document in st.session_state.selected_docs:
            st.markdown(
                f"""
                <div class="source-card">
                    <div class="source-name">
                        📄 {document}
                    </div>
                </div
                """,
                unsafe_allow_html= True
            )
    else:
        for index, source in enumerate(st.session_state.sources):
            with source_columns[index%3]:
                st.markdown(
                    f"""
                    <div class="source-card">
                        <div class="source-name">
                            📄 {source["sources"]}
                        </div>
                        <div class="source-page">
                            Page {source["page"]}
                        </div>
                    </div
                    """,
                    unsafe_allow_html= True
                )     
        
def get_document_chunks(all_chunks, filename):
    document_chunks= [
        chunk
        for chunk in all_chunks
        if chunk.metadata.get("source")== filename
    ] 

    return document_chunks


   



        

            


