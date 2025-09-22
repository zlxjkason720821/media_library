#include "mainwindow.h"
#include <QVBoxLayout>
#include <QSqlQuery>
#include <QLabel>
#include <QPushButton>
#include <QPixmap>
#include <QMessageBox>
#include <cstdlib>

#ifdef _WIN32
const QString PLAYER_PATH = "C:/Program Files/DAUM/PotPlayer/PotPlayerMini64.exe";
#endif

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    resize(1100, 750);

    QWidget *central = new QWidget(this);
    QVBoxLayout *mainLayout = new QVBoxLayout(central);

    // 搜索框
    searchBox = new QLineEdit(this);
    searchBox->setPlaceholderText("🔍 输入关键字搜索...");
    mainLayout->addWidget(searchBox);

    // 分类选择
    categoryBox = new QComboBox(this);
    categoryBox->addItem("推荐");
    categoryBox->addItem("Actors");
    categoryBox->addItem("Anime");
    categoryBox->addItem("MMD");
    categoryBox->addItem("Producers");
    categoryBox->addItem("Voice");
    categoryBox->addItem("JAV");
    categoryBox->addItem("Special");
    mainLayout->addWidget(categoryBox);

    // 滚动区域
    QScrollArea *scrollArea = new QScrollArea(this);
    gridWidget = new QWidget(scrollArea);
    gridLayout = new QGridLayout(gridWidget);
    scrollArea->setWidget(gridWidget);
    scrollArea->setWidgetResizable(true);
    mainLayout->addWidget(scrollArea);

    setCentralWidget(central);

    // 数据库连接
    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("videos.db");
    if (!db.open()) {
        QMessageBox::critical(this, "错误", "无法打开数据库");
        return;
    }

    // 初始加载推荐
    loadRecommendations();

    // 连接信号槽
    connect(searchBox, &QLineEdit::returnPressed, [=]() {
        searchVideos(searchBox->text());
    });
    connect(categoryBox, &QComboBox::currentTextChanged, this, &MainWindow::loadByCategory);
}

MainWindow::~MainWindow() {
    db.close();
}

void MainWindow::clearGrid() {
    QLayoutItem *item;
    while ((item = gridLayout->takeAt(0)) != nullptr) {
        delete item->widget();
        delete item;
    }
}

void MainWindow::loadRecommendations() {
    clearGrid();
    QSqlQuery query("SELECT id, display_name, filepath, thumbnail FROM videos ORDER BY play_count ASC, RANDOM() LIMIT 20");

    int row = 0, col = 0;
    while (query.next()) {
        int id = query.value(0).toInt();
        QString title = query.value(1).toString();
        QString filepath = query.value(2).toString();
        QString thumb = query.value(3).toString();

        QLabel *thumbLabel = new QLabel;
        QPixmap pix(thumb);
        thumbLabel->setPixmap(pix.scaled(200, 120, Qt::KeepAspectRatio));
        thumbLabel->setAlignment(Qt::AlignCenter);

        QLabel *titleLabel = new QLabel(title);
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("color:white;");

        QPushButton *playBtn = new QPushButton("▶ 播放");
        connect(playBtn, &QPushButton::clicked, [=]() {
            playVideo(filepath, id);
        });

        QWidget *card = new QWidget;
        QVBoxLayout *vbox = new QVBoxLayout(card);
        vbox->addWidget(thumbLabel);
        vbox->addWidget(titleLabel);
        vbox->addWidget(playBtn);

        gridLayout->addWidget(card, row, col);
        col++;
        if (col >= 4) { col = 0; row++; }
    }
}

void MainWindow::loadByCategory(const QString &category) {
    if (category == "推荐") {
        loadRecommendations();
        return;
    }

    clearGrid();
    QSqlQuery query;
    query.prepare("SELECT id, display_name, filepath, thumbnail FROM videos WHERE category=? ORDER BY play_count ASC, RANDOM() LIMIT 20");
    query.addBindValue(category);
    query.exec();

    int row = 0, col = 0;
    while (query.next()) {
        int id = query.value(0).toInt();
        QString title = query.value(1).toString();
        QString filepath = query.value(2).toString();
        QString thumb = query.value(3).toString();

        QLabel *thumbLabel = new QLabel;
        QPixmap pix(thumb);
        thumbLabel->setPixmap(pix.scaled(200, 120, Qt::KeepAspectRatio));
        thumbLabel->setAlignment(Qt::AlignCenter);

        QLabel *titleLabel = new QLabel(title);
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("color:white;");

        QPushButton *playBtn = new QPushButton("▶ 播放");
        connect(playBtn, &QPushButton::clicked, [=]() {
            playVideo(filepath, id);
        });

        QWidget *card = new QWidget;
        QVBoxLayout *vbox = new QVBoxLayout(card);
        vbox->addWidget(thumbLabel);
        vbox->addWidget(titleLabel);
        vbox->addWidget(playBtn);

        gridLayout->addWidget(card, row, col);
        col++;
        if (col >= 4) { col = 0; row++; }
    }
}

void MainWindow::searchVideos(const QString &keyword) {
    clearGrid();
    QSqlQuery query;
    query.prepare("SELECT id, display_name, filepath, thumbnail FROM videos WHERE display_name LIKE ? LIMIT 20");
    query.addBindValue("%" + keyword + "%");
    query.exec();

    int row = 0, col = 0;
    while (query.next()) {
        int id = query.value(0).toInt();
        QString title = query.value(1).toString();
        QString filepath = query.value(2).toString();
        QString thumb = query.value(3).toString();

        QLabel *thumbLabel = new QLabel;
        QPixmap pix(thumb);
        thumbLabel->setPixmap(pix.scaled(200, 120, Qt::KeepAspectRatio));
        thumbLabel->setAlignment(Qt::AlignCenter);

        QLabel *titleLabel = new QLabel(title);
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("color:white;");

        QPushButton *playBtn = new QPushButton("▶ 播放");
        connect(playBtn, &QPushButton::clicked, [=]() {
            playVideo(filepath, id);
        });

        QWidget *card = new QWidget;
        QVBoxLayout *vbox = new QVBoxLayout(card);
        vbox->addWidget(thumbLabel);
        vbox->addWidget(titleLabel);
        vbox->addWidget(playBtn);

        gridLayout->addWidget(card, row, col);
        col++;
        if (col >= 4) { col = 0; row++; }
    }
}

void MainWindow::playVideo(const QString &filepath, int videoId) {
#ifdef _WIN32
    QString cmd = "\"" + PLAYER_PATH + "\" \"" + filepath + "\"";
    system(cmd.toStdString().c_str());
#else
    QMessageBox::information(this, "播放", "视频路径: " + filepath);
#endif

    // 更新播放次数
    QSqlQuery update;
    update.prepare("UPDATE videos SET play_count = play_count + 1, last_watched = CURRENT_TIMESTAMP WHERE id=?");
    update.addBindValue(videoId);
    update.exec();
}