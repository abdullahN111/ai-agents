from agents import function_tool
from utils.database import SessionLocal
from utils import models



@function_tool
def add_task(task_name: str, task_description: str, task_deadline: str):
    """Add a task by using task_name: str (print task name Capitalize i.e Task), task_description: str (print task description Capitalize i.e This is my Task) and task_deadline: str (print deadline date in dd-mm-yyyy format no matter what the user provides)"""
    db = SessionLocal()
    try:
        new_task = models.Task(
            title=task_name,
            description=task_description,
            deadline=task_deadline
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return f"✅ Added: #{new_task.id} {new_task.title} | {new_task.deadline}"
    except Exception as e:
        db.rollback()
        return f"❌ Failed to add task: {e}"
    finally:
        db.close()
        
        
@function_tool
def view_all_tasks():
    """Fetch and view all tasks from database"""
    db = SessionLocal()
    try:
        tasks = db.query(models.Task).all()
        if not tasks:
            return {"message": "📂 No tasks found."}
        task_list = [f"- #{task.id} {task.title} | {task.deadline}" for task in tasks]
       
        for task in tasks:
            print(f"- #{task.id} {task.title} | {task.deadline}")
       
        return {"message": "Here is the list of all your tasks:", "tasks": task_list}
    except Exception as e:
        return {"error": f"❌ Failed to fetch tasks: {e}"}
    finally:
        db.close()

@function_tool
def view_single_task(id: int):
    """Fetch and View a task from database by using id: int"""
    db = SessionLocal()
    try:
        task = db.query(models.Task).filter(models.Task.id == id).first()
        if not task:
            return f"⚠️ Task {id} not found."
           
        return f"📌 #{task.id}: {task.title} | {task.deadline}\n {task.description}"
       
    except Exception as e:
        return f"❌ Failed to fetch task: {e}"
    finally:
        db.close()

@function_tool
def delete_task(id: int):
    """Delete a task by using id: int"""
    db = SessionLocal()
    try:
        task = db.query(models.Task).filter(models.Task.id == id).first()
        if not task:
           
            return f"⚠️ Task {id} not found."
        db.delete(task)
        db.commit()
        return f"🗑️ Deleted task #{id}"
    except Exception as e:
        db.rollback()
        return f"❌ Failed to delete task: {e}"
    finally:
        db.close()


@function_tool
def greet_user(name: str):
    """Takes a name: str and print greetings with options"""
    print(f"\n--Hey {name}! Please select an option--\n")
    options = ["Add Task", "View All Tasks", "View Single Task", "Delete Task", "Exit"]
    for index, option in enumerate(options):
        return f"{index+1}. {option}"
    