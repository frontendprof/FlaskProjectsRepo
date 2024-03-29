from flask import Flask,redirect,url_for
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname,join
import secrets
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user



app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/abdlmalik/Desktop/Flask/UltimateFlask/Admin-Flask/admin_db.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


db = SQLAlchemy(app)
admin=Admin(app,name='BurgerCafe',template_mode='bootstrap3')
login_manager=LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    age = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
    	return '<User %r>' % (self.username)



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.id)

class UserView(ModelView):
	# column_exclude_list = ['password' ]
	column_display_pk = True
	can_create = True
	can_edit = False
	can_delete = False
	can_export=True


	def on_model_change(self, form, model, is_created):
		model.password = generate_password_hash(model.password, method='sha256')
	inline_models=[Comment]


	def is_accessible(self):
		return current_user.is_authenticated
         
	def inaccessible_callback(self, name, **kwargs):
		return '<h1>You are not logged in!</h1>'


class CommentView(ModelView):
	create_modal=True

class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notification.html')

admin.add_view(UserView(User,db.session))
admin.add_view(CommentView(Comment, db.session))

path=join(dirname(__file__),'uploads')
admin.add_view(FileAdmin(path,'/uploads/',name='UploadHere'))
admin.add_view(NotificationsView(name='Notifications', endpoint='notify'))


@app.route('/login')
def login():
    user = User.query.filter_by(id=1).first()
    login_user(user)
    return redirect(url_for('admin.index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))




if __name__ == '__main__':
    app.run(debug=True)