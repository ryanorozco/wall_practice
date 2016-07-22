from system.core.controller import *

class Sessions(Controller):

    def index(self):
        return self.load_view('index.html')

    def register(self):
        self.load_model('User')
        self.models['User'].registerUser(request.form)
        return redirect('/')

    def login(self):
        self.load_model('User')
        userArray = self.models['User'].loginUser(request.form)
        if userArray:
            session['currentUser'] = userArray[0]
            return redirect ('/wall')
        else:
            return redirect('/')

    def wall(self):
        self.load_model('User')
        messageArray = self.models['User'].displayMessage()
        commentArray = self.models['User'].displayComment()
        return self.load_view('wall.html', messageArray=messageArray, commentArray=commentArray)

    def message(self):
        self.load_model('User')
        self.models['User'].postMessage(request.form)
        return redirect('/wall')

    def comment(self):
        self.load_model('User')
        self.models['User'].postComment(request.form)
        return redirect('/wall')

    def logout(self):
        session.pop('currentUser', None)
        return redirect('/')
