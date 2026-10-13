from src.database.db_config import supabase
import bcrypt
import hashlib

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def get_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()

def create_user_account(name, email, password):
    data= { 'name': name, 'email': email, 'password': hash_pass(password)}
    response= supabase.table('profiles').insert(data).execute()
    return response.data

def check_user_exist(email):
    response= supabase.table('profiles').select('email').eq('email', email).execute()
    return len(response.data)>0   

def user_login_db(email, password):
    response= supabase.table('profiles').select('*').eq('email',email).execute()
    if response.data:
        user= response.data[0]
        if check_pass(password, user['password']):
            return user
        else:
            return False
    else:
        return None

def store_uploaded_files(file_name,user_id, file_bytes, file_hash= None):
    if file_hash is None:
        file_hash= get_file_hash(file_bytes)
    
    existing_user_file= supabase.table('documents').select('*').eq('user_id', user_id).eq('file_hash', file_hash).execute()
    existing_file= supabase.table('documents').select('*').eq('file_hash', file_hash).execute()

    if len(existing_user_file.data)>0:
        print(f"Duplicate found: {file_name}- skipping DB insert and ingestion")
        return False
    
    storage_path= f"{user_id}/{file_name}"
    supabase.storage.from_("documents").upload(
        path= storage_path,
        file= file_bytes,
        file_options={"upsert": "true"}
    )

    data= {
        'filename': file_name,
        'user_id': user_id,
        'file_hash': file_hash,
        'storage_path': storage_path
    }
    response= supabase.table('documents').insert(data).execute()
    if len(existing_file.data)>0:
        return "file_exist"
    return True

def get_documents(user_id):
    response= supabase.table('documents').select("*").eq('user_id', user_id).order('created_at', desc= True).execute()
    return response.data

def conversations(user_id, title):
    data= {
        'user_id': user_id,
        'title': title
    }
    response= supabase.table('conversations').insert(data).execute()
    return response.data

def find_conversations(user_id):
    response= supabase.table('conversations').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
    return response.data

def store_messages(conversation_id, user_query):
    data= {
        'conversation_id': conversation_id,
        'content': user_query
    }
    response= supabase.table('messages').insert(data).execute()
    return response.data

def get_conversation_messages(conversation_id):
    response= supabase.table('messages').select('*').eq('conversation_id', conversation_id).order('created_at', desc=True).execute()
    return response.data