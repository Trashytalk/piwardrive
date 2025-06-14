#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <ctype.h>

static PyObject* parse_coords(PyObject* self, PyObject* args) {
    const char* text;
    Py_ssize_t len;
    if (!PyArg_ParseTuple(args, "s#", &text, &len)) {
        return NULL;
    }

    PyObject* list = PyList_New(0);
    const char* p = text;
    const char* end = text + len;

    while (p < end) {
        while (p < end && isspace((unsigned char)*p)) {
            p++;
        }
        if (p >= end) break;

        char* q;
        double lon = strtod(p, &q);
        p = q;
        if (p < end && *p == ',') p++;
        double lat = strtod(p, &q);
        p = q;
        if (p < end && *p == ',') {
            strtod(p + 1, &q); // skip altitude
            p = q;
        }
        PyObject* tup = Py_BuildValue("(dd)", lat, lon);
        PyList_Append(list, tup);
        Py_DECREF(tup);
        while (p < end && !isspace((unsigned char)*p)) {
            p++;
        }
    }

    return list;
}

static PyMethodDef methods[] = {
    {"parse_coords", parse_coords, METH_VARARGS, "Parse KML coordinate string"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef ckmlmodule = {
    PyModuleDef_HEAD_INIT,
    "ckml",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_ckml(void) {
    return PyModule_Create(&ckmlmodule);
}
