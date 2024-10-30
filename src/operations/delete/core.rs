//! Defines the core functions for deleting records. These functions should not be called directly
//! from the Python API but rather from the TCP connection in the runtime module. In this
//! module we can do the following:
//!
//! * Delete a record in the database
//!
//! # Notes
//! The unit tests for the delete operation can be found in the `tests` module in the create core module.
use crate::connection::interface::WrappedConnection;
use surrealdb::opt::Resource;
use surrealdb::sql::Range;
use surrealdb::RecordId;

/// Delete all records, or a specific record
///
/// # Arguments
/// * `connection_id` - The connection performing the operation on the database
/// * `resource` - The resource to delete (can be a table or a range)
///
/// # Returns
///
pub async fn delete(connection: WrappedConnection, resource: String) -> Result<String, String> {
    let response = match resource.parse::<RecordId>() {
        Ok(rid) => connection
            .connection
            .delete(Resource::RecordId(rid))
            .await
            .map_err(|e| e.to_string())?,
        Err(_) => connection
            .connection
            .delete(Resource::Table(resource))
            .await
            .map_err(|e| e.to_string())?,
    };
    Ok(response.into_inner().into_json().to_string())
}
