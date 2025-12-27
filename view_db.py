
from app import app, db, User, PredictionHistory

def show_data():
    with app.app_context():
        # Ensure tables exist (useful if app hasn't been hit yet)
        db.create_all()
        
        print("\n--- Registered Users ---")
        users = User.query.all()
        if not users:
            print("No users found.")
        else:
            for u in users:
                print(f"ID: {u.id} | Username: {u.username} | Email: {u.email}")

        print("\n--- Recent Predictions ---")
        preds = PredictionHistory.query.limit(5).all()
        if not preds:
            print("No prediction history found.")
        else:
            for p in preds:
                print(f"ID: {p.id} | Item: {p.item_type_str} | Predicted Sales: {p.prediction:.2f}")

if __name__ == "__main__":
    show_data()
