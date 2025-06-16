#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>

static PyObject* py_haversine_distance(PyObject* self, PyObject* args) {
    double lat1, lon1, lat2, lon2;
    if (!PyArg_ParseTuple(args, "(dd)(dd)", &lat1, &lon1, &lat2, &lon2)) {
        return NULL;
    }
    double r = 6371000.0;
    double phi1 = lat1 * M_PI / 180.0;
    double phi2 = lat2 * M_PI / 180.0;
    double d_phi = (lat2 - lat1) * M_PI / 180.0;
    double d_lambda = (lon2 - lon1) * M_PI / 180.0;
    double a = sin(d_phi / 2) * sin(d_phi / 2) +
               cos(phi1) * cos(phi2) * sin(d_lambda / 2) * sin(d_lambda / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    double dist = r * c;
    return PyFloat_FromDouble(dist);
}

static PyObject* py_polygon_area(PyObject* self, PyObject* args) {
    PyObject* seqObj;
    if (!PyArg_ParseTuple(args, "O", &seqObj)) {
        return NULL;
    }
    PyObject* seq = PySequence_Fast(seqObj, "expected sequence of (lat, lon)");
    if (!seq) return NULL;
    Py_ssize_t n = PySequence_Fast_GET_SIZE(seq);
    if (n < 3) {
        Py_DECREF(seq);
        return PyFloat_FromDouble(0.0);
    }
    double sum_lat = 0.0, sum_lon = 0.0;
    for (Py_ssize_t i = 0; i < n; ++i) {
        PyObject* item = PySequence_Fast_GET_ITEM(seq, i);
        double lat, lon;
        if (!PyArg_ParseTuple(item, "dd", &lat, &lon)) {
            Py_DECREF(seq);
            return NULL;
        }
        sum_lat += lat;
        sum_lon += lon;
    }
    double lat0 = sum_lat / n;
    double lon0 = sum_lon / n;
    double cos_lat0 = cos(lat0 * M_PI / 180.0);
    PyObject* item = PySequence_Fast_GET_ITEM(seq, n - 1);
    double latp, lonp;
    if (!PyArg_ParseTuple(item, "dd", &latp, &lonp)) {
        Py_DECREF(seq);
        return NULL;
    }
    double prev_x = (lonp - lon0) * cos_lat0;
    double prev_y = latp - lat0;
    double area = 0.0;
    for (Py_ssize_t i = 0; i < n; ++i) {
        item = PySequence_Fast_GET_ITEM(seq, i);
        double lat, lon;
        if (!PyArg_ParseTuple(item, "dd", &lat, &lon)) {
            Py_DECREF(seq);
            return NULL;
        }
        double x = (lon - lon0) * cos_lat0;
        double y = lat - lat0;
        area += prev_x * y - x * prev_y;
        prev_x = x;
        prev_y = y;
    }
    Py_DECREF(seq);
    area = fabs(area) / 2.0;
    double meter_per_deg = 111320.0;
    double res = area * meter_per_deg * meter_per_deg;
    return PyFloat_FromDouble(res);
}

static PyObject* py_point_in_polygon(PyObject* self, PyObject* args) {
    double lat, lon;
    PyObject* polyObj;
    if (!PyArg_ParseTuple(args, "(dd)O", &lat, &lon, &polyObj)) {
        return NULL;
    }
    PyObject* seq = PySequence_Fast(polyObj, "expected sequence of (lat, lon)");
    if (!seq) return NULL;
    Py_ssize_t n = PySequence_Fast_GET_SIZE(seq);
    if (n < 3) {
        Py_DECREF(seq);
        Py_RETURN_FALSE;
    }
    int inside = 0;
    for (Py_ssize_t i = 0; i < n; ++i) {
        PyObject* p1 = PySequence_Fast_GET_ITEM(seq, i);
        PyObject* p2 = PySequence_Fast_GET_ITEM(seq, (i + 1) % n);
        double lat1, lon1, lat2, lon2;
        if (!PyArg_ParseTuple(p1, "dd", &lat1, &lon1) ||
            !PyArg_ParseTuple(p2, "dd", &lat2, &lon2)) {
            Py_DECREF(seq);
            return NULL;
        }
        if ((lon1 > lon) != (lon2 > lon)) {
            double intersect = (lat2 - lat1) * (lon - lon1) /
                               (lon2 - lon1 + 1e-12) + lat1;
            if (lat < intersect)
                inside = !inside;
        }
    }
    Py_DECREF(seq);
    if (inside)
        Py_RETURN_TRUE;
    Py_RETURN_FALSE;
}

static PyMethodDef methods[] = {
    {"haversine_distance", py_haversine_distance, METH_VARARGS, "Great-circle distance in meters"},
    {"polygon_area", py_polygon_area, METH_VARARGS, "Polygon area in square meters"},
    {"point_in_polygon", py_point_in_polygon, METH_VARARGS, "Test if point inside polygon"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cgeommodule = {
    PyModuleDef_HEAD_INIT,
    "cgeom",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_cgeom(void) {
    return PyModule_Create(&cgeommodule);
}

