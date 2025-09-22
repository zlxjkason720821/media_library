#pragma once
#include <QMainWindow>
#include <QSqlDatabase>
#include <QGridLayout>
#include <QScrollArea>
#include <QLineEdit>
#include <QComboBox>

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void loadRecommendations();
    void loadByCategory(const QString &category);
    void searchVideos(const QString &keyword);
    void playVideo(const QString &filepath, int videoId);

private:
    QSqlDatabase db;
    QWidget *gridWidget;
    QGridLayout *gridLayout;
    QLineEdit *searchBox;
    QComboBox *categoryBox;
    void clearGrid();
};