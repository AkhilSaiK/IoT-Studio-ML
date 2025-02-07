import couchdb
from train import COUCH_URL, DB_NAME

def view_database():
    try:
        # Connect to CouchDB
        couch = couchdb.Server(COUCH_URL)
        db = couch[DB_NAME]
        
        # Get all documents
        all_docs = {}
        
        print("\nDatabase Contents:")
        print("-" * 50)
        
        for doc_id in db:
            doc = db[doc_id]
            doc_type = doc.get('type', 'unknown')
            
            # Don't print the actual data/model content as it's too large
            doc_summary = {
                'type': doc_type,
                'id': doc_id,
            }
            
            if doc_type == 'dataset':
                doc_summary.update({
                    'filename': doc.get('filename'),
                    'file_type': doc.get('file_type'),
                    'upload_timestamp': doc.get('upload_timestamp'),
                    'created_timestamp': doc.get('created_timestamp')
                })
            elif doc_type == 'model':
                doc_summary.update({
                    'model_type': doc.get('model_type'),
                    'dataset_name': doc.get('dataset_name'),
                    'timestamp': doc.get('timestamp'),
                    'metrics': doc.get('metrics')
                })
                
            all_docs[doc_id] = doc_summary
            
            print(f"\nDocument ID: {doc_id}")
            for key, value in doc_summary.items():
                if key != 'id':
                    print(f"{key}: {value}")
            print("-" * 50)
            
        return all_docs
        
    except Exception as e:
        print(f"Error viewing database: {str(e)}")
        return None

if __name__ == "__main__":
    view_database() 