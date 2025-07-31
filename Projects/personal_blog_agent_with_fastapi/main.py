from blog_agent.main import get_response
from utils import models, database

def main():
    db_gen = database.get_db()
    db = next(db_gen)

    print("\n📝 Welcome to the AI Blog Assistant 📝")
    print("-----------------------")
    options = ["Post Blog", "Get Blog", "Delete Blog", "Get All Blogs", "Exit"]
    for index, option in enumerate(options):
        print(f"{index+1}. {option}")
    print("-----------------------")

    condition = True
    while condition:
        try:
            user_input = input("\n📥 Please choose an option (1-5 or name): ").strip().lower()
        except Exception as e:
            print(f"⚠️ Error: {e}")
            continue

        if user_input in ["exit", "5"]:
            condition = False
            break

        elif user_input in ["1", "post blog"]:
            topic = input("\nEnter the topic for the new blog: ").strip()
            if not topic:
                print("❌ Topic cannot be empty.")
                continue
            response = get_response(topic)
            final_output = response.final_output  

            new_blog = models.Blog(title=topic.upper(), body=final_output)
            db.add(new_blog)
            db.commit()
            db.refresh(new_blog)

            print(f"✅ Blog posted successfully with ID {new_blog.id}!")

        elif user_input in ["2", "get blog"]:
            query = input("Enter blog ID or title to view: ").strip()
            try:
                blog_id = int(query)
                response = get_response(f"view blog {blog_id}")
            except ValueError:
                response = get_response(f"view blog {query}")

            print("\n📖 Blog:\n")
            print(response.final_output)

        elif user_input in ["3", "delete blog"]:
            blog_id = input("Enter blog ID to delete: ").strip()
            blog = db.query(models.Blog).filter(models.Blog.id == int(blog_id)).first()
            if blog:
                db.delete(blog)
                db.commit()
                print("🗑️ Blog deleted successfully.")
            else:
                print("❌ Blog not found.")

        elif user_input in ["4", "get all blogs"]:
            blogs = db.query(models.Blog).all()
            print("\n📚 All Blogs:\n")
            for blog in blogs:
                print(f"➡️ ID: {blog.id} | Title: {blog.title}")

        else:
            print("❌ Invalid input. Please select a valid option (1-5).")

    print("\n👋 Thank you for using the AI Blog Assistant. Goodbye!\n")
    db_gen.close()

if __name__ == "__main__":
    main()
