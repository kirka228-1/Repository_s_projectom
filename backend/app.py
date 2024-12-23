from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Course, Assignment, Grade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/eso_db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        new_user = User(name=name, email=email, password=password, role=role)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('home'))

@app.route('/courses')
def list_courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        teacher_id = session['user_id']
        new_course = Course(title=title, description=description, teacher_id=teacher_id)

        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('list_courses'))
    
    return render_template('create_course.html')

@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
    return redirect(url_for('list_courses'))

@app.route('/assignments/<int:course_id>', methods=['GET', 'POST'])
def manage_assignments(course_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        new_assignment = Assignment(title=title, description=description, due_date=due_date, course_id=course_id)

        db.session.add(new_assignment)
        db.session.commit()
        return redirect(url_for('manage_assignments', course_id=course_id))
    
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    return render_template('assignments.html', assignments=assignments, course_id=course_id)

@app.route('/delete_assignment/<int:assignment_id>')
def delete_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
    return redirect(url_for('manage_assignments', course_id=assignment.course_id))

@app.route('/grade_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def grade_assignment(assignment_id):
    if request.method == 'POST':
        grade = request.form['grade']
        user_id = request.form['user_id']
        new_grade = Grade(assignment_id=assignment_id, user_id=user_id, grade=grade)
        
        db.session.add(new_grade)
        db.session.commit()
        return redirect(url_for('manage_assignments', course_id=Assignment.query.get(assignment_id).course_id))
    
    users = User.query.filter_by(role='student').all()
    return render_template('grade_assignment.html', assignment_id=assignment_id, users=users)

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    courses = Course.query.filter((Course.teacher_id == user_id) | (Course.students.any(id=user_id))).all()
    return render_template('profile.html', user=user, courses=courses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
