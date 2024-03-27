# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from aqt.qt import QTabWidget, QVBoxLayout, QLabel, QWidget, QFont, QGroupBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QCoreApplication, QMetaObject, QAbstractItemView

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(605, 872)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTitle = QLabel(Dialog)
        self.labelTitle.setObjectName(u"labelTitle")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.labelTitle.setFont(font)

        self.verticalLayout.addWidget(self.labelTitle)

        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabOptions = QWidget()
        self.tabOptions.setObjectName(u"tabOptions")
        self.verticalLayout_4 = QVBoxLayout(self.tabOptions)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.tabOptions)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableWidgetFilteredDecks = QTableWidget(self.groupBox)
        if (self.tableWidgetFilteredDecks.columnCount() < 2):
            self.tableWidgetFilteredDecks.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidgetFilteredDecks.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidgetFilteredDecks.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidgetFilteredDecks.setObjectName(u"tableWidgetFilteredDecks")

        self.verticalLayout_2.addWidget(self.tableWidgetFilteredDecks)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBoxImport = QGroupBox(self.tabOptions)
        self.groupBoxImport.setObjectName(u"groupBoxImport")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxImport)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBoxImportSublayout1 = QHBoxLayout()
        self.groupBoxImportSublayout1.setObjectName(u"groupBoxImportSublayout1")
        self.buttonImport = QPushButton(self.groupBoxImport)
        self.buttonImport.setObjectName(u"buttonImport")

        self.groupBoxImportSublayout1.addWidget(self.buttonImport)

        self.groupBoxImportSpacer = QSpacerItem(398, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.groupBoxImportSublayout1.addItem(self.groupBoxImportSpacer)


        self.verticalLayout_3.addLayout(self.groupBoxImportSublayout1)

        self.tableWidgetStagedForImportFilteredDecks = QTableWidget(self.groupBoxImport)
        if (self.tableWidgetStagedForImportFilteredDecks.columnCount() < 3):
            self.tableWidgetStagedForImportFilteredDecks.setColumnCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidgetStagedForImportFilteredDecks.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidgetStagedForImportFilteredDecks.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidgetStagedForImportFilteredDecks.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        self.tableWidgetStagedForImportFilteredDecks.setObjectName(u"tableWidgetStagedForImportFilteredDecks")

        self.verticalLayout_3.addWidget(self.tableWidgetStagedForImportFilteredDecks)


        self.verticalLayout_4.addWidget(self.groupBoxImport)

        self.groupBoxExport = QGroupBox(self.tabOptions)
        self.groupBoxExport.setObjectName(u"groupBoxExport")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBoxExport)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBoxExportLayout = QHBoxLayout()
        self.groupBoxExportLayout.setObjectName(u"groupBoxExportLayout")
        self.buttonExportSelected = QPushButton(self.groupBoxExport)
        self.buttonExportSelected.setObjectName(u"buttonExportSelected")

        self.groupBoxExportLayout.addWidget(self.buttonExportSelected)

        self.groupBoxExportSpacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.groupBoxExportLayout.addItem(self.groupBoxExportSpacer1)

        self.pushButtonExportAll = QPushButton(self.groupBoxExport)
        self.pushButtonExportAll.setObjectName(u"pushButtonExportAll")

        self.groupBoxExportLayout.addWidget(self.pushButtonExportAll)

        self.groupBoxExportSpacer2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.groupBoxExportLayout.addItem(self.groupBoxExportSpacer2)

        self.groupBoxExportLayout.setStretch(3, 4)

        self.horizontalLayout_5.addLayout(self.groupBoxExportLayout)


        self.verticalLayout_4.addWidget(self.groupBoxExport)

        self.tabWidget.addTab(self.tabOptions, "")
        self.tabAbout = QWidget()
        self.tabAbout.setObjectName(u"tabAbout")
        self.verticalLayout_6 = QVBoxLayout(self.tabAbout)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tabAboutLayout = QVBoxLayout()
        self.tabAboutLayout.setObjectName(u"tabAboutLayout")
        self.labelWrittenBy = QLabel(self.tabAbout)
        self.labelWrittenBy.setObjectName(u"labelWrittenBy")

        self.tabAboutLayout.addWidget(self.labelWrittenBy)

        self.tabAboutSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tabAboutLayout.addItem(self.tabAboutSpacer)


        self.verticalLayout_6.addLayout(self.tabAboutLayout)

        self.tabWidget.addTab(self.tabAbout, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.dialogLayout = QHBoxLayout()
        self.dialogLayout.setObjectName(u"dialogLayout")
        self.dialogSpacer = QSpacerItem(408, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.dialogLayout.addItem(self.dialogSpacer)

        self.buttonOkay = QPushButton(Dialog)
        self.buttonOkay.setObjectName(u"buttonOkay")

        self.dialogLayout.addWidget(self.buttonOkay)

        self.buttonExit = QPushButton(Dialog)
        self.buttonExit.setObjectName(u"buttonExit")

        self.dialogLayout.addWidget(self.buttonExit)


        self.verticalLayout.addLayout(self.dialogLayout)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.labelTitle.setText(QCoreApplication.translate("Dialog", u"Filtered Deck Manager", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Filtered Decks", None))
        ___qtablewidgetitem = self.tableWidgetFilteredDecks.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Deck Name", None));
        ___qtablewidgetitem1 = self.tableWidgetFilteredDecks.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Deck ID", None));
        self.groupBoxImport.setTitle(QCoreApplication.translate("Dialog", u"Import", None))
        self.buttonImport.setText(QCoreApplication.translate("Dialog", u"Import", None))
        ___qtablewidgetitem2 = self.tableWidgetStagedForImportFilteredDecks.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Deck Name", None));
        ___qtablewidgetitem3 = self.tableWidgetStagedForImportFilteredDecks.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Estimated Card Count", None));
        ___qtablewidgetitem4 = self.tableWidgetStagedForImportFilteredDecks.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Tags", None));
        self.groupBoxExport.setTitle(QCoreApplication.translate("Dialog", u"Export", None))
        self.buttonExportSelected.setText(QCoreApplication.translate("Dialog", u"Export Selected", None))
        self.pushButtonExportAll.setText(QCoreApplication.translate("Dialog", u"Export All", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOptions), QCoreApplication.translate("Dialog", u"Options", None))
        self.labelWrittenBy.setText(QCoreApplication.translate("Dialog", u"Written by Arvind Draffen, 2024", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAbout), QCoreApplication.translate("Dialog", u"About", None))
        self.buttonOkay.setText(QCoreApplication.translate("Dialog", u"Okay", None))
        self.buttonExit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi

