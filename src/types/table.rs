use pyo3::{pyclass, pymethods};

use crate::types::resource::Resource;

#[pyclass]
pub struct Table(String);

#[pymethods]
impl Table {
    #[new]
    pub fn new(value: String) -> Self {
        Self(value)
    }
}
