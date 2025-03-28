"""Modules to create UI."""
import random
import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator, QKeySequence
from PySide2.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlRelationalDelegate,
    QSqlRelationalTableModel,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

# pylint: disable=import-error
import movies_csv_data

DATABASE_NAME: str
HOST_NAME: str
USER_NAME: str
PASSWORD: str
PORT: int


# pylint: disable=too-many-instance-attributes
class CSVWin(QMainWindow):
    """This class launches UI and creates Movie DB connection."""

    def __init__(self) -> None:
        super().__init__()

        self.quit_action = QAction("Exit")
        self.quit_action.setShortcut(QKeySequence("Ctrl+Q"))

        self.file_menu = self.menuBar().addMenu("File")

        self.title = QLabel("Movies DB")

        self.add_button = QPushButton("Add Movie")
        self.del_button = QPushButton("Delete Movie")

        self.less_more_than_combobox = QComboBox()
        self.value_lineedit = QLineEdit()
        self.filter_audience_score = {"All": "", "less_than": "<", "more_than": ">"}

        self.sort_combobox = QComboBox()

        self.filter_combobox = QComboBox()

        self.search_lineeit = QLineEdit()

        self.table_view = QTableView()

        self.widget = QWidget()
        self.main_h_layout = QHBoxLayout()
        self.main_h_layout.addWidget(self.add_button)
        self.main_h_layout.addWidget(self.del_button)
        self.main_h_layout.addStretch()
        self.main_h_layout.addWidget(self.search_lineeit)
        self.main_h_layout.addStretch()
        self.main_h_layout.addWidget(self.less_more_than_combobox)
        self.main_h_layout.addWidget(self.value_lineedit)
        self.main_h_layout.addStretch()
        self.main_h_layout.addWidget(self.sort_combobox)
        self.main_h_layout.addWidget(self.filter_combobox)

        self.main_v_layout = QVBoxLayout(self.widget)
        self.main_v_layout.addWidget(self.title, Qt.AlignmentFlag.AlignLeft)  # type: ignore
        self.main_v_layout.addLayout(self.main_h_layout)
        self.main_v_layout.addWidget(self.table_view)

        self.setCentralWidget(self.widget)

        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("CSV Model View Example")

        self.create_connection()
        self.model = QSqlRelationalTableModel()
        self.model.setTable("movies")
        self.setup_window()
        self.setup_table()

    @staticmethod
    def create_connection() -> None:
        """This function creates a Movie DB connection with postgres driver"""
        database = QSqlDatabase.addDatabase("QPSQL")
        database.setDatabaseName(DATABASE_NAME)
        database.setHostName(HOST_NAME)
        database.setUserName(USER_NAME)
        database.setPassword(PASSWORD)
        database.setPort(PORT)

        if not database.open():
            print("Unable to open data source file")
            sys.exit(1)

        tables_needed = {"movies"}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            QMessageBox.critical(
                None,
                "Error",
                f"""<p>The following tables are 
                missing from the database: {tables_not_found}</p>""",
            )  # type: ignore
            sys.exit(1)

    def setup_window(self) -> None:
        """This Function sets the QMainWidget connections,
        button connections, table delegates, table models."""

        # QMainWidget file menu - connections.
        self.quit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.quit_action)

        # Title settings.
        self.title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.title.setStyleSheet("font: bold 24px")

        # Delete items from DB - connections.
        self.add_button.clicked.connect(self.add_item)
        self.del_button.clicked.connect(self.delete_item)

        # Audience Score lineedit - settings and connections.
        self.value_lineedit.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.value_lineedit.setPlaceholderText("Mention Audience Score")
        self.value_lineedit.setValidator(QIntValidator(0, 100))
        self.value_lineedit.textEdited.connect(self.audience_score_filter)

        # Less or More Than combobox - connections.
        self.less_more_than_combobox.addItems(self.filter_audience_score.keys())  # type: ignore

        # Sorting Movie Table columns - options and connections.
        sort_options = [
            "Sort by Film ID",
            "Sort by Film Name",
            "Sort by Genre",
            "Sort by Lead Studio",
            "Sort by Profitability",
            "Sort by Rotten Tomatoes",
            "Sort by Worldwide",
            "Sort by Year",
        ]
        self.sort_combobox.addItems(sort_options)
        self.sort_combobox.currentTextChanged.connect(self.set_sorting_order)

        # Filter Genre - options and connections.
        filter_options = list(set(movies_csv_data.genre))
        filter_options.insert(0, "All")
        self.filter_combobox.addItems(filter_options)
        self.filter_combobox.currentIndexChanged.connect(self.genre_filter)

        # Search Movie - options and connections.
        self.search_lineeit.setPlaceholderText("Mention Movie Name")
        self.search_lineeit.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.search_lineeit.textEdited.connect(self.film_name_filter)

        # Set Table model, horizontal and vertical header, selection behavior
        self.table_view.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_view.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_view.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Delegate - set table delegate
        delegate = QSqlRelationalDelegate()
        self.table_view.setItemDelegate(delegate)

    def setup_table(self) -> None:
        """This function sets the headers of the Movie DB tables."""

        self.model.setHeaderData(
            self.model.fieldIndex("id"), Qt.Orientation.Horizontal, "Film ID"
        )
        self.model.setHeaderData(
            self.model.fieldIndex("film"), Qt.Orientation.Horizontal, "Film Name"
        )
        self.model.setHeaderData(
            self.model.fieldIndex("genre"), Qt.Orientation.Horizontal, "Genre"
        )
        self.model.setHeaderData(
            self.model.fieldIndex("lead_studios"),
            Qt.Orientation.Horizontal,
            "Lead Studios",
        )
        self.model.setHeaderData(
            self.model.fieldIndex("audience_score_percent"),
            Qt.Orientation.Horizontal,
            "Audience Score %",
        )
        self.model.setHeaderData(
            self.model.fieldIndex("profitability"),
            Qt.Orientation.Horizontal,
            "Profitability",
        )
        self.model.setHeaderData(
            self.model.fieldIndex("rotten_tomatoes_percent"),
            Qt.Orientation.Horizontal,
            "Rotten Tomatoes %",
        )
        self.model.setHeaderData(
            self.model.fieldIndex("worldwide_gross"),
            Qt.Orientation.Horizontal,
            "Worldwide Gross $",
        )
        self.model.setHeaderData(
            self.model.fieldIndex("year"), Qt.Orientation.Horizontal, "Year"
        )

        self.model.select()

    def add_item(self) -> None:
        """Add a new record to the last row of the table."""

        last_row = self.model.rowCount()
        self.model.insertRow(last_row)
        query = QSqlQuery()
        query.exec_("SELECT MAX (id) FROM movies")
        film_ids = random.randint(1000, 2500)
        self.model.setData(
            self.model.index(last_row, self.model.fieldIndex("film_id")), film_ids
        )
        if query.next():
            int(query.value(0))

    def delete_item(self) -> None:
        """This function deletes the items from Movie DB."""
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()

    def set_sorting_order(self, text: str) -> None:
        """This function sorts the Movie DB table columns.

        Args:
            text: Sorting Options from Combobox.

        """

        if text == "Sort by Film ID":
            self.model.setSort(
                self.model.fieldIndex("id"), Qt.SortOrder.AscendingOrder
            )
        elif text == "Sort by Film Name":
            self.model.setSort(
                self.model.fieldIndex("film"), Qt.SortOrder.AscendingOrder
            )
        elif text == "Sort by Genre":
            self.model.setSort(
                self.model.fieldIndex("genre"), Qt.SortOrder.AscendingOrder
            )
        elif text == "Sort by Lead Studio":
            self.model.setSort(
                self.model.fieldIndex("lead_studios"), Qt.SortOrder.AscendingOrder
            )
        elif text == "Sort by Profitability":
            self.model.setSort(
                self.model.fieldIndex("profitability"), Qt.SortOrder.AscendingOrder
            )
        elif text == "Sort by Rotten Tomatoes":
            self.model.setSort(
                self.model.fieldIndex("rotten_tomatoes_percent"), Qt.SortOrder.AscendingOrder
            )
        elif text == "Sort by Worldwide":
            self.model.setSort(
                self.model.fieldIndex("worldwide_gross"), Qt.SortOrder.AscendingOrder
            )
        elif text == "Sort by Year":
            self.model.setSort(
                self.model.fieldIndex("year"), Qt.SortOrder.AscendingOrder
            )

        self.model.select()

    def genre_filter(self) -> None:
        """This function filters Movie DB as per Genre."""
        selected_filter = self.filter_combobox.currentText()
        if selected_filter == "All":
            self.model.setFilter("")
        else:
            self.model.setFilter(f"genre = '{selected_filter}'")
        self.model.select()

    def film_name_filter(self) -> None:
        """This function lets you search for movies in Movie DB."""
        search_text = self.search_lineeit.text()
        if not search_text:
            self.model.setFilter("")
        else:
            self.model.setFilter(f"film LIKE '%{search_text}%'")
        self.model.select()

    def audience_score_filter(self) -> None:
        """This function lets you filter movies as per movie audience score in Movie DB."""
        value = self.less_more_than_combobox.currentText()
        score = self.value_lineedit.text()
        if not score or value == "All":
            self.model.setFilter(self.filter_audience_score["All"])
        else:
            operator = self.filter_audience_score[value]
            self.model.setFilter(f"audience_score_percent {operator} {score}")
        self.model.select()
