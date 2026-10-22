# d1_550_description

Unitree D1-T(d1_550)アームのURDFを、ベンダー提供のROS1/Gazebo Classic向けパッケージから
ROS2(ament_cmake + xacro)/gz sim向けに移植したもの。Go2_deploy Issue #65。

## 出典とライセンス

- 取得元: Unitreeの配布CDN(ベンダー提供の `d1_550_description`)。STLメッシュ9個
  (`meshes/`)はベンダー提供物をそのまま含む
- `package.xml` の `<license>BSD</license>` は、取得元の表記を引き継いだ値。
  **ベンダー側のライセンス・再配布条件は未確認**(このリポジトリはpublic)。
  確認が取れるまで、メッシュの再配布可否は不明として扱うこと
- 移植時の変更: ROS2化(CMakeLists/package.xml)、xacro化、ros2_control用の調整など

## 未検証事項

- 関節の回転軸の向きは実機未照合(同じベンダーURDFで2軸が実機と不一致だったという
  報告がある。Go2_deploy Issue #64 で実機確認する)
- 重力はsimで無効化している(`go2_description/xacro/gazebo.xacro` 参照。暫定回避)
