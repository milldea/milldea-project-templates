# milldea-project-templates

## 概要

このリポジトリは、ミルディアでプロジェクトを新規作成する際のテンプレートを保存/更新していくリポジトリです。
ある程度テンプレート化しておくことで、プロジェクトの開始を早めたり、他のプロジェクトに参画する際に理解が早まることなどを目的としています。

## 方針

テンプレート準備の方針は以下の通りですが、あくまで方針なので必須ではありません

* sample で環境構築ができたことを確認できる状態にする
  * 例
    * xxx コマンドを実行すると、 hello world が出力される
* Reamde の準備
  * sample の動作に必要な手順を記載する
  * ディレクトリ構成を記載する
  * 注意点、過去プロジェクトでハマった点などを記載する
  * 新規で環境構築した際の手順などもメモしておく
    * 例
      * node プロジェクトなら 
      * `npm init` などのコマンド
* Docker 上に構築できるようにして、環境依存を減らす
* Class 設計などの細かい内容は書かない
  * 誰にもメンテできないオレオレフレームワークみたいなものにしたくない
* 指針でしかないので、古臭くなったテンプレートはすぐに捨てましょう


# テンプレート
## spec

設計のテンプレート

## serverless

serverless framework を使うプロジェクト

### python

serverless-python

（以下などを随時拡張していきたい...）

## Flutter

## Flask

## Azure App Service

### node.js