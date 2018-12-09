# Flask_MusicDB



### First for the group menbers

---

- If you are a member in my group, just ask for the rest of the project. I only uploaded part of the project for security reason. 
- This is for better communication and distribution for front end and back end. 
- Follow the instructions below to get the whole project working if you are a collaborator of this project



### Instructions

---

First, find an empty directory, e.g `/Github/myProject/ERG3010_project`, as the working directory.

Use the `cd` command in the terminal (bash) to switch to the working directory. 

```bash
$ cd xxx/.../xxx/Github/myProject/ERG3010_project
```

Then, use the commands below to initiallize the git and  link the repo on Github

```bash
$ git init
$ git remote add origin https://github.com/EricYJA/Flask_MusicDB.git
```

After that, use the command below to get the project on GitHub

```bash
$ git pull origin master
```

Now, you have the things online in your working directory.



Then, use the project you have already had in your local PC, add the rest of the project in the working directory, done. Then, activate the virtual environment using `pipenv`. The `Pipfile and Pipfile.lock` must be in the working directory when you are trying to run the command below. Note that the `--dev` is for creating a seperated environment. 

```bash
$ pipenv install --dev
```

Use the command below to get into the virtual environemnt. 

```bash
$ pipenv shell
```

Make sure you are now in the virtual environment. Use the command below to run the flask project.

```bash
$ flask run
```

Great! Start working, partner. 



### VERY IMPORTANT !!!

---

When trying to push and refresh the program on the Github. DO NOT use the command below. 

```bash
git add . 
```

ONLY add the files you have changed into the staging area. Good luck!


###The singer's songs I have in the server

- 李健

    沧海轻舟
    假如爱有天意

- 张国荣
    
    月亮代表我的心
    你这样恨我