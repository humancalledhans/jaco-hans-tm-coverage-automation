from src.tm_partners.operations.reset_selected_table_row import reset_selected_table_row
from src.tm_partners.operations.reset_current_db_row import reset_current_db_row

def reset_singletons():
    """Helper to reset all the relevant singletons with temporary data
    """
    reset_current_db_row()
    reset_selected_table_row()