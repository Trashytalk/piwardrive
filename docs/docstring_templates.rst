Docstring Templates
===================

All public functions should use the NumPy style shown below.

Example
-------

.. code-block:: python

   def sync_new_records(db_path: str, url: str, *, state_file: str | None = None,
                        timeout: int = 30, retries: int = 3) -> int:
       """Synchronise new records to a remote server.

       Parameters
       ----------
       db_path : str
           Path to the local SQLite database.
       url : str
           Destination upload URL.
       state_file : str or None, optional
           File storing the last synced row ID (default is ``db_path + '.last'``).
       timeout : int, optional
           Request timeout in seconds.
       retries : int, optional
           Number of retry attempts on failure.

       Returns
       -------
       int
           Count of records uploaded.
       """

