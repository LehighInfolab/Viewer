Tutorial

Adding and running an executable to the backend

1. Add a route to index.js to handle a call.
  1. An example of this is _router.get('/vasp', function(req, res, next) {…}_
  2. '/vasp' is the name of the call from the frontend – this can be called anything.
2. Create a child that holds the executable call.
  1. Use _const child = spawn(…)_
    1. Use 'executables' path for the last parameter of spawn() to point to the correct path for executables.
3. Must add _child.on('error')_ to avoid errors.
  1. Can also add _child.on('close'), child.stdout.on(), child.stderr.on()_ for debugging.
4. In /views folder, add a reference to the route call from above.
  1. For example, if route call is '/vasp', then _form(action='/vasp' method ='POST')_
5. Add your executable files to /executables
  1. The call to the executable will be exactly what your call is from the terminal. This would be the easiest way to run the executable. For example,

```
constchild = spawn('python', ['./DiffBond\_v2.py', '-i', '../public/uploads/1brs.pdb', '-m', 'i'], executables)
```

