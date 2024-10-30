use pyo3::{pyclass, pymethods};


#[pyclass]
pub struct Table(String);

#[pymethods]
impl Table {
    #[new]
    pub fn new(value: String) -> Self {
        Self(value)
    }
}
