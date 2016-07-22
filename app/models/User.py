from system.core.model import Model
from flask import Flask, flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

class User(Model):

    def registerUser(self, userData):
        hasErrors = False
        if len(userData['firstName']) < 2:
            flash(u'Name must be 2 or more characters!',"regerror")
            hasErrors = True
        elif len(userData['lastName']) < 2:
            flash(u'Last Name must be 2 or more characters!', "regerror")
            hasErrors = True
        elif not EMAIL_REGEX.match(userData['email']):
            flash(u'You entered an invalid email!', "regerror")
            hasErrors = True
        elif not hasErrors:
            sql = 'INSERT INTO users (first_name, last_name, email_address, password, created_at, updated_at) VALUES (:firstName, :lastName, :email, :password, NOW(), NOW())'
            data = {
                    'firstName': userData['firstName'],
                    'lastName': userData['lastName'],
                    'email': userData['email'],
                    'password': userData['password']
                    }
            return self.db.query_db(sql, data)

    def loginUser(self, userData):
        query = 'SELECT * FROM users WHERE email_address = :email AND password = :password'
        data = {
                'email': userData['email'],
                'password': userData['password']
                }
        return self.db.query_db(query, data)

    def postMessage(self, userData):
        sql = 'INSERT INTO messages (message, user_id, created_at, updated_at) VALUES (:message, :userId, NOW(), NOW())'
        data = {
                'message': userData['message'],
                'userId': userData['userId']
                }
        return self.db.query_db(sql, data)

    def displayMessage(self):
        query = 'SELECT m.id AS msgID, message, m.created_at AS messageTime, m.user_id, u.id, u.first_name AS messageFirstName, u.last_name AS messageLastName FROM messages m LEFT JOIN users u ON m.user_id=u.id ORDER BY m.created_at DESC'
        return self.db.query_db(query)

    def postComment(self, userData):
        sql = 'INSERT INTO comments (comment, message_id, user_id, created_at, updated_at) VALUES (:comment, :messageId, :userId, NOW(), NOW())'
        data = {
                'comment': userData['comment'],
                'messageId': userData['msgId'],
                'userId': userData['userId']
                }
        return self.db.query_db(sql, data)

    def displayComment(self):
        query = 'SELECT c.comment,u.first_name, u.last_name, c.created_at AS commentTime, c.user_id AS commenterID, c.message_id, m.id, m.message, m.created_at, m.user_id FROM comments c LEFT JOIN messages m ON c.message_id=m.id LEFT JOIN users u ON c.user_id=u.id ORDER BY commentTime'
        return self.db.query_db(query)
