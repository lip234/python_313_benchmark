// A simple Python C-extension module

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

static PyObject* dummy_cat(PyObject *self, PyObject *args);
static PyMethodDef DummyMethods[] = {
    {"cat",  dummy_cat, METH_VARARGS,
     "Concatenate two strings."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef dummymodule = {
    PyModuleDef_HEAD_INIT,
    "dummy",
    NULL,
    -1,
    DummyMethods
};


PyMODINIT_FUNC PyInit_dummy(void) {
    PyObject *m;
    m = PyModule_Create(&dummymodule);
    return m;
}

static PyObject* dummy_cat(PyObject *self, PyObject *args) {
    char *s1, *s2;
    int s1_len, s2_len;
    char *buffer;
    if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse arguments");
        return NULL;
    }
    // Release the GIL and pretend to do some CPU-intense task. Only do so around code that does not access Python objects.
    // This will allow other Python threads to run.
    Py_BEGIN_ALLOW_THREADS
    s1_len = strlen(s1);
    s2_len = strlen(s2);
    buffer = calloc(s1_len + s2_len + 1, 1);
    if (buffer != NULL) {
        memcpy(buffer, s1, s1_len);
        memcpy(buffer+s1_len, s2, s2_len);
    }

    // Re-acquire the GIL
    Py_END_ALLOW_THREADS
    if (buffer == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to allocate memory");
        return NULL;
    }
    return PyUnicode_FromString(buffer);
}

