from flask import *
from flask_sqlalchemy import *
from flask_migrate import *
from sqlalchemy import *
from werkzeug.utils import *
import os
import random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:123@localhost/instagram'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = True
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config["SECRET_KEY"] = "instagram-web-programing"
ALLOW_EXTENSION = {'png', 'jpg', 'jpeg', 'webp', 'avif', 'mp4'}
db = SQLAlchemy(app)

migrate = Migrate(app, db)


def check_file(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOW_EXTENSION
    return value and type_file


def user_folder():
    folder = 'static/img/user_img/'
    return folder


def post_folder():
    folder = 'static/img/puplication/'
    return folder


user_post = db.Table('user_posted_table',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     )

commentary_table = db.Table('user_commentary_table',
                            db.Column('user_comment_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('commentary_user_id', db.Integer, db.ForeignKey('commentary.id'))
                            )

comment_post = db.Table('comment_post',
                        db.Column('post_comment_id', db.Integer, db.ForeignKey('posts.id')),
                        db.Column('commentary_id', db.Integer, db.ForeignKey('commentary.id'))
                        )

like_table = db.Table('user_post_like',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                      )

save_table = db.Table('user_post_save',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                      )

follow = db.Table('chanel_table',
                  db.Column('chanel_id', db.Integer, db.ForeignKey('chanel.id')),
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                  )

friends_table = db.Table('table_friends',
                         db.Column('friends_id', db.Integer, db.ForeignKey('friends.id')),
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                         )


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    bio = Column(String)
    photo = Column(String)
    followers = Column(Integer)
    following = Column(Integer)
    publications = Column(Integer)
    post = db.relationship('Posts', backref='user', secondary=user_post, order_by="Posts.id")
    save = db.relationship('Posts', backref='user_save', secondary=save_table, order_by="Posts.id")
    like_user = db.relationship('Posts', backref='user_like', secondary=like_table, order_by="Posts.id")
    commentary = db.relationship('Commentary', backref='user', secondary=commentary_table, order_by="Commentary.id")


class Chanel(db.Model):
    __tablename__ = 'chanel'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    follow_user = db.relationship('User', backref='chanel', secondary=follow, order_by="User.id")


class Friends(db.Model):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    friends_user = db.relationship('User', backref='friends', secondary=friends_table, order_by="User.id")


class Posts(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    file = Column(String)
    bio = Column(String)
    like = Column(Integer)
    length_comment = Column(Integer)
    comment = db.relationship('Commentary', backref='posts', secondary=comment_post, order_by="Commentary.id")


class Commentary(db.Model):
    __tablename__ = 'commentary'
    id = Column(Integer, primary_key=True)
    comment = Column(String)


def rec_user():
    user_now = User.query.filter(User.username == session['username']).first()
    all_user = User.query.all()
    for chanel_id in user_now.chanel:
        id_ch = User.query.filter(User.id == chanel_id.id).first()
        all_user.remove(id_ch)
    return all_user


def follow_user(user_id):
    user_1 = User.query.filter(User.id == user_id).first()
    user_list = []
    for chanel in user_1.chanel:
        user_2 = User.query.filter(User.id == chanel.id).first()
        user_list.append(user_2)
    return user_list


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone_email')
        username = request.form.get('username')
        password = request.form.get('password')
        login_user = request.form.get('login')
        register = request.form.get('reg')
        error_phone = User.query.filter(User.phone == phone).first()
        error_username = User.query.filter(User.username == username).first()
        if register:
            if name and phone and username and password and (not error_username) and (not error_phone):
                photo_url = '/static/img/web_img/defoult_user_img.png'
                add_user = User(name=name, username=username, password=password, phone=phone, photo=photo_url,
                                followers=0, following=0, publications=0, bio='')
                creat_chanel = Chanel(name=username)
                creat_friends = Friends(name=username)
                db.session.add_all([creat_friends, add_user, creat_chanel])
                db.session.commit()
                session['username'] = username
                return redirect(url_for('edit_user'))
            else:
                return redirect(url_for('login', error='Fill all correct !'))
        elif login_user:
            if username and password:
                check_user = User.query.filter(User.username == username).first()
                if check_user.password == password:
                    session['username'] = check_user.username
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('login', error='Wrong password !'))
            else:
                return redirect(url_for('login', error='Fill all correct !'))
    return render_template('login.html')


@app.route('/index')
def index():
    user_now = User.query.filter(User.username == session['username']).first()
    followers = Chanel.query.filter(Chanel.id == user_now.id).first()
    a = Posts.query.order_by(desc(Posts.id)).all()
    b = Posts.query.order_by(desc(Posts.like)).all()
    random_list = [a, b]
    all_post = random.choice(random_list)
    recomend_user = User.query.all()
    return render_template('index.html', all_post=all_post, recomend=recomend_user, user_now=user_now,
                           followers=followers, rec_user=rec_user())


@app.route('/save/<int:post_id>')
def save(post_id):
    user_now = User.query.filter(User.username == session['username']).first()
    post_now = Posts.query.filter(Posts.id == post_id).first()
    user_now.save.append(post_now)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_save/<int:post_id>')
def delete_save(post_id):
    user_now = User.query.filter(User.username == session['username']).first()
    post_now = Posts.query.filter(Posts.id == post_id).first()
    user_now.save.remove(post_now)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_friends/<int:user_id>')
def add_friends(user_id):
    user_now = User.query.filter(User.username == session['username']).first()
    user_add = User.query.filter(User.id == user_id).first()
    user_friends = Friends.query.filter(Friends.id == user_now.id).first()
    user_friends.friends_user.append(user_add)
    db.session.commit()
    return redirect(url_for('user'))


@app.route('/delete_friends/<int:user_id>')
def delete_friends(user_id):
    user_now = User.query.filter(User.username == session['username']).first()
    user_add = User.query.filter(User.id == user_id).first()
    user_friends = Friends.query.filter(Friends.id == user_now.id).first()
    user_friends.friends_user.remove(user_add)
    db.session.commit()
    return redirect(url_for('user'))


@app.route('/delete_all_friends')
def delete_all_friends():
    user_now = User.query.filter(User.username == session['username']).first()
    user_friends = Friends.query.filter(Friends.id == user_now.id).first()
    user_friends.friends_user.clear()
    db.session.commit()
    return redirect(url_for('user'))


@app.route('/follow/<int:user_id>')
def follow(user_id):
    user_now = User.query.filter(User.username == session['username']).first()
    user_follow = User.query.filter(User.id == user_id).first()
    user_chanel = Chanel.query.filter(Chanel.id == user_follow.id).first()
    user_chanel.follow_user.append(user_now)
    following = user_now.following + 1
    User.query.filter(User.username == session['username']).update({
        "following": following
    })
    followers = user_follow.followers + 1
    User.query.filter(User.id == user_id).update({
        "followers": followers
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_follow/<int:user_id>')
def delete_follow(user_id):
    user_now = User.query.filter(User.username == session['username']).first()
    user_follow = User.query.filter(User.id == user_id).first()
    user_chanel = Chanel.query.filter(Chanel.id == user_follow.id).first()
    user_chanel.follow_user.remove(user_now)
    following = user_now.following - 1
    User.query.filter(User.username == session['username']).update({
        "following": following
    })
    followers = user_follow.followers - 1
    User.query.filter(User.id == user_id).update({
        "followers": followers
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_comment/<int:post_id>', methods=['POST', 'GET'])
def add_comment(post_id):
    user_now = User.query.filter(User.username == session['username']).first()
    post_now = Posts.query.filter(Posts.id == post_id).first()
    comment = request.form.get('comment')
    add = Commentary(comment=comment)
    db.session.add(add)
    db.session.commit()
    user_now.commentary.append(add)
    post_now.comment.append(add)
    db.session.commit()
    length_comment = len(post_now.comment)
    Posts.query.filter(Posts.id == post_id).update({
        'length_comment': length_comment
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_like/<int:post_id>')
def add_like(post_id):
    post_now = Posts.query.filter(Posts.id == post_id).first()
    user_now = User.query.filter(User.username == session['username']).first()
    user_now.like_user.append(post_now)
    like_user = post_now.like + 1
    Posts.query.filter(Posts.id == post_id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_like/<int:post_id>')
def delete_like(post_id):
    post_now = Posts.query.filter(Posts.id == post_id).first()
    user_now = User.query.filter(User.username == session['username']).first()
    user_now.like_user.remove(post_now)
    like_user = post_now.like - 1
    Posts.query.filter(Posts.id == post_id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/window_reels/<int:post_id>')
def window_reels(post_id):
    post_now = Posts.query.filter(Posts.id == post_id).first()
    user_now = User.query.filter(User.username == session['username']).first()
    followers = Chanel.query.filter(Chanel.id == user_now.id).first()
    all_post = Posts.query.order_by(desc(Posts.like)).all()
    recomend_user = User.query.all()
    return render_template('reels_window.html', post_now=post_now, user_now=user_now, all_post=all_post,
                           recomend=recomend_user, followers=followers)


@app.route('/another_user/<int:user_id>')
def another_user(user_id):
    user_now = User.query.filter(User.username == session['username']).first()
    if user_id == user_now.id:
        return redirect(url_for('user'))
    another = User.query.filter(User.id == user_id).first()
    another_chanel = Chanel.query.filter(Chanel.id == user_id).first()
    all_user = User.query.all()
    user_user_post = []
    for post in another.post:
        user_user_post.append(post)
    return render_template('another_user.html', user=another, user_now=user_now, user_post=user_user_post,
                           all_user=all_user, another_chanel=another_chanel,
                           follow_user=follow_user(user_id), rec_user=rec_user())


@app.route('/user')
def user():
    user_now = User.query.filter(User.username == session['username']).first()
    followers = Chanel.query.filter(Chanel.id == user_now.id).first()
    user_now_followers = len(followers.follow_user)
    friend = Friends.query.filter(Friends.id == user_now.id).first()
    all_friends = len(friend.friends_user)
    User.query.filter(User.username == session['username']).update({
        "followers": user_now_followers
    })
    chanel_user = Chanel.query.filter(Chanel.id == user_now.id).first()
    user_now_post = []
    for post in user_now.post:
        user_now_post.append(post)
    return render_template('user.html', user=user_now, user_now=user_now, user_post=user_now_post,
                           follow_user=follow_user(user_now.id), another_chanel=chanel_user, friends=friend,
                           all_friends=all_friends)


@app.route('/reels')
def reels():
    user_now = User.query.filter(User.username == session['username']).first()
    all_post = Posts.query.order_by(desc(Posts.like)).all()
    followers = Chanel.query.filter(Chanel.id == user_now.id).first()
    return render_template('reels.html', user_now=user_now, all_post=all_post, followers=followers)


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    user_now = User.query.filter(User.username == session['username']).first()
    bio = request.form.get('bio')
    photo = request.files['img']
    folder = post_folder()
    if photo and check_file(photo.filename) and bio:
        photo_file = secure_filename(photo.filename)
        photo_url = '/' + folder + photo_file
        app.config['UPLOAD_FOLDER'] = folder
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        creat_post = Posts(file=photo_url, bio=bio, like=0, length_comment=0)
        db.session.add(creat_post)
        db.session.commit()
        user_now.post.append(creat_post)
        db.session.commit()
        User.query.filter(User.username == session['username']).update({
            "publications": len(user_now.post)
        })
        db.session.commit()
    else:
        return redirect(url_for('index', error='Fill all correct !'))
    return redirect(url_for('index'))


@app.route('/edit_user', methods=['POST', 'GET'])
def edit_user():
    user_now = User.query.filter(User.username == session['username']).first()
    if request.method == 'POST':
        edit_img = request.form.get('edit_img')
        edit_info = request.form.get('edit_info')
        if edit_img:
            photo = request.files['img']
            folder = user_folder()
            if photo and check_file(photo.filename):
                photo_file = secure_filename(photo.filename)
                photo_url = '/' + folder + photo_file
                app.config['UPLOAD_FOLDER'] = folder
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
                User.query.filter(User.id == user_now.id).update({
                    'photo': photo_url
                })
                db.session.commit()
        elif edit_info:
            name = request.form.get('name')
            phone = request.form.get('phone_email')
            username = request.form.get('username')
            password = request.form.get('password')
            bio = request.form.get('bio')
            if name and password and phone and username:
                User.query.filter(User.id == user_now.id).update({
                    'name': name,
                    'phone': phone,
                    'username': username,
                    'password': password,
                    'bio': bio
                })
                db.session.commit()
            else:
                return redirect(url_for('edit_user', error='Fill all correct !'))
        return redirect(url_for('edit_user'))
    return render_template('edit_user.html', user_now=user_now)


@app.route('/log_out')
def log_out():
    session['username'] = ''
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
