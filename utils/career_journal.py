from google.cloud import firestore

db = firestore.Client()
collection = db.collection("career_journal")

#SAVEING THE JOURNAL ENTRY TO FIRESTORE
def save_journal_entry(entry):

    doc_ref = collection.add({"entry": entry})
    return doc_ref
#RETRUEVING JOURNAL ENTRIES
def view_journal_entries():

    docs = collection.stream()
    return [doc.to_dict()["entry"] for doc in docs]



