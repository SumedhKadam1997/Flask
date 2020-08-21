We are putting too much code in the app.py file, we've already seen how we can
put the forms in their own .py script file. Let's explore how we could expand
this organization further for larger flask projects.


├───app.py # main app.py file to be called to start server for web app
├───requirements.txt # File of pip install statements for your app
├───migrations # folder created for migrations by calling
├───myproject # main project folder, sub-components will be in separate folders
│   │   data.sqlite
│   │   models.py
│   │   __init__.py
│   │
│   ├───owners
│   │   │   forms.py
│   │   │   views.py
│   │   │
│   │   ├───templates
│   │      └───owners
│   │             add_owner.html
│   │   
│   │
│   ├───puppies
│   │   │   forms.py
│   │   │   views.py
│   │   │
│   │   ├───templates
│   │   │   └───puppies
│   │   │           add.html
│   │   │           delete.html
│   │   │           list.html
│   │
│   ├───static # Where you store your CSS, JS, Images, Fonts, etc...
│   ├───templates
│          base.html
│          home.html
