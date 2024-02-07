# OpenDAPI and Woven - Tutorial

This example demonstrates how to integrate an app with OpenDAPI and later with Woven's service. The tutorial will walkthrough the following:
* Making changes to an existing model.
* Creating a new model.
* Setting up OpenDAPI / Woven integration from scratch

Check out this walkthrough video
[![Watch the video](https://img.youtube.com/vi/3q2fI9siGHs/maxresdefault.jpg)](https://youtu.be/3q2fI9siGHs)

## Making changes to an existing model.
In the Todos app, we have a basic pynamodb model, for which the DAPI files and woven integration checks are already setup.

This scenario demonstrates day to day use of OpenDAPI and integration with Woven.

Steps:
* Clone the repository https://github.com/WovenCollab/dapi-demo
* Create a local branch
  ```bash
  $ git checkout -b model-edit
  ```
* Add a field `user_id` to the model `todos/todo_model.py:TodoModel`.
  ```diff
  diff --git a/todos/todo_model.py b/todos/todo_model.py
  index 6febbc9..99255ec 100644
  --- a/todos/todo_model.py
  +++ b/todos/todo_model.py
  @@ -14,7 +14,7 @@ class TodoModel(Model):
             host = None


     checked = BooleanAttribute(null=False)
     updatedAt = UTCDateTimeAttribute(null=False)
  +  user_id = UnicodeAttribute(null=False)
  ```
* Commit the change and push the change upstream
  ```bash
  $ git add todo_model.py
  $ git commit -m "Added a field to tracker owner of todo"
  $ git push origin model-edit
  ```
* Create a pull request
  https://github.com/WovenCollab/dapi-demo/pull/new/model-edit

You should now see the `OpenDAPI CI` check running in the PR.

If you notice, we did not run `make test` to generate the dapi files. Let us do that now

* Run tests
  ```bash
  (.venv)$ make test
  poetry run pytest -s -vv
  ============================= test session starts ==============================
  ...

  tests/test_opendapi.py::test_and_autoupdate_dapis PASSED

  ============================== 1 passed in 7.60s ===============================
  (.venv)$ git status
  On branch model-edit
  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working directory)
    	modified:   dapis/pynamodb/todos.dapi.yaml


  $ git diff
   ...
      is_nullable: false
      is_pii: false
      access: private
   +- name: user_id
   +  data_type: string
   +  description: Placeholder - Please correct
   +  is_nullable: false
   +  is_pii: true
   +  access: private
  ```

As you can see, the dapi file has been updated to reflect the model change.

* Edit the dapi file to update the placeholder information, commit it and push it to the remote branch
  ```bash
  $ git commit -m "Generated dapi file"
  $ git push origin model-edit
  ```

* The OpenDapi checks will run again with the pull request. If you click through the check details, you can see how the Dapi check interacts with the Woven api servers to validate your changes.

### Triggering an error with a model change.
Let us now try to trigger a scenario which demonstrates the utility of our checks.

* Edit a model and make a PII column as nullable.
```diff
diff --git a/todos/todo_model.py b/todos/todo_model.py
index 6febbc9..99255ec 100644
--- a/todos/todo_model.py
+++ b/todos/todo_model.py
@@ -14,7 +14,7 @@ class TodoModel(Model):
             host = None

     todo_id = UnicodeAttribute(hash_key=True, null=False)
-    text = UnicodeAttribute(null=False)
+    text = UnicodeAttribute(null=True)
     checked = BooleanAttribute(null=False)
```

* Edit the dapi file to reflect this.
```diff
diff --git a/dapis/pynamodb/todos.dapi.yaml b/dapis/pynamodb/todos.dapi.yaml
index 1213a24..8c82940 100644
--- a/dapis/pynamodb/todos.dapi.yaml
+++ b/dapis/pynamodb/todos.dapi.yaml
@@ -30,7 +30,7 @@ fields:
 - name: text
   data_type: string
   description: The entry for the todo action
-  is_nullable: false
+  is_nullable: true
   is_pii: true
   access: private
 - name: todo_id
```

* Commit the changes and push it up.
```bash
$ git add todos/todo_model.py
$ git add dapis/pynamodb/todos.dapi.yaml
$ git commit -m "Make notes field nullable"
$ git push origin model-edit
```
