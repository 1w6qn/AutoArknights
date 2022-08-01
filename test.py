class c:
    def post(cgi,**data):
        def deco(func):
            def w():
                func()
                return b
            return w
        print(cgi)
        return deco
    @post('cccc',b=1)
    def a():print('pass')
