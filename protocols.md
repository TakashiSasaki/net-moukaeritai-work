# 会話ドキュメント: サービス検出プロトコルまとめ

## 目次

1. はじめに
2. mDNS, SSDP, UPnP の概要と関係
3. SSDP メッセージ例
4. SSDP の利用シチュエーション
5. WS-Discovery の概要
6. 各プロトコルのマルチキャストアドレスとポート
7. 同一マルチキャストアドレス使用の理由
8. 標準化文書によるアドレス予約
9. まとめ
10. 参考文献

---

## 1. はじめに

本ドキュメントは、mDNS、SSDP、UPnP、WS-Discovery といったローカルネットワークのサービス検出プロトコルに関する会話内容を整理し、要点ごとにまとめたものです。

## 2. mDNS, SSDP, UPnP の概要と関係

* **mDNS (Multicast DNS)**: ローカルネットワーク上で DNS クエリ／レスポンスをマルチキャスト(224.0.0.251:5353／ff02::fb:5353) でやり取りし、名前解決と DNS-SD によるサービス検出を行う。
* **SSDP (Simple Service Discovery Protocol)**: HTTP-over-UDP(HTTPU) ベースで M-SEARCH/NOTIFY メッセージを 239.255.255.250:1900／\[ff02::c]:1900 に送信し、UPnP デバイスやサービス検出を行う。
* **UPnP (Universal Plug and Play)**: SSDP をディスカバリ層として採用し、検出後に HTTP(SOAP) での制御や GENA イベント通知を行うフレームワーク。
* **関係**: mDNS と SSDP は独立した検出プロトコル。UPnP は SSDP を利用。機器によっては両方に対応し、相互運用性を高める。

## 3. SSDP メッセージ例

1. **M-SEARCH リクエスト**

```
M-SEARCH * HTTP/1.1
HOST: 239.255.255.250:1900
MAN: "ssdp:discover"
MX: 3
ST: ssdp:all
```

2. **M-SEARCH レスポンス**

```
HTTP/1.1 200 OK
CACHE-CONTROL: max-age=1800
DATE: Tue, 29 Jul 2025 12:00:00 GMT
EXT:
LOCATION: http://192.168.1.100:80/description.xml
SERVER: Linux/5.10 UPnP/1.1 MyDevice/2.0
ST: urn:schemas-upnp-org:device:MediaServer:1
USN: uuid:1234...::urn:schemas-upnp-org:device:MediaServer:1
```

3. **NOTIFY アナウンス**

* *ssdp\:alive*:

```
NOTIFY * HTTP/1.1
HOST: 239.255.255.250:1900
CACHE-CONTROL: max-age=1800
LOCATION: http://192.168.1.100:80/description.xml
NT: urn:schemas-upnp-org:service:ContentDirectory:1
NTS: ssdp:alive
USN: uuid:1234...::urn:schemas-upnp-org:service:ContentDirectory:1
```

* *ssdp\:byebye*:

```
NOTIFY * HTTP/1.1
HOST: 239.255.255.250:1900
NT: urn:schemas-upnp-org:service:ContentDirectory:1
NTS: ssdp:byebye
USN: uuid:1234...::urn:schemas-upnp-org:service:ContentDirectory:1
```

## 4. SSDP の利用シチュエーション

* **DLNA メディア機器**: NAS、スマートテレビ、メディアサーバがメディア共有を実現。
* **UPnP IGD**: ルーターがポートフォワーディング設定を自動化。
* **Windows SSDP Discovery サービス**: ネットワークプリンターやストレージの検出。
* **ネットワークプリンター**: Brother、Xerox などが自らアナウンス。
* **IoT/スマートホーム**: 照明、スピーカー、IP カメラの検出。

## 5. WS-Discovery の概要

* **WS-Discovery**: SOAP-over-UDP を用い、Probe/ProbeMatch でサービス探索、Hello/Bye で状態通知を行う OASIS 標準。
* **メッセージフロー**:

  1. Probe (マルチキャスト)
  2. ProbeMatch (ユニキャスト応答)
  3. Hello / Bye (マルチキャスト生存・離脱通知)
* **利用例**: Windows WSDMON によるプリンター検出、ONVIF IP カメラ検出。

## 6. 各プロトコルのマルチキャストアドレスとポート

|     プロトコル    |   IPv4 マルチキャスト  | IPv6 マルチキャスト |      ポート     |
| :----------: | :-------------: | :----------: | :----------: |
|     mDNS     |   224.0.0.251   |   ff02::fb   |   UDP 5353   |
|     SSDP     | 239.255.255.250 |    ff02::c   |   UDP 1900   |
| WS-Discovery | 239.255.255.250 |    ff02::c   | TCP/UDP 3702 |

## 7. 同一マルチキャストアドレス使用の理由

* **239.255.255.250** は IANA が「ローカルサービス検出用」に予約した管理スコープアドレス。
* 両プロトコル共通で利用することで、ネットワーク設定や実装の単純化、相互運用性を向上。
* ポート番号とメッセージ形式でプロトコルを区別。

## 8. 標準化文書によるアドレス予約

* **RFC 2365** “Administratively Scoped IP Multicast”: 239.0.0.0/8 を管理スコープとして定義。
* **UPnP Device Architecture v1.1**: SSDP 用アドレスとして 239.255.255.250 を指定。
* **OASIS WS-Discovery v1.1**: WS-Discovery で 239.255.255.250 および ff02::c を使用と明記。

## 9. まとめ

本会話を通じて、mDNS、SSDP、UPnP、WS-Discovery の概要、相互関係、実際のメッセージ例、利用シチュエーション、アドレス・ポート情報、および標準化背景を整理しました。

## 10. 参考文献

1. RFC 2365 “Administratively Scoped IP Multicast”
2. UPnP Forum, “UPnP Device Architecture v1.1”
3. OASIS, “Web Services Dynamic Discovery (WS-Discovery) v1.1”
4. IANA, “Multicast Address Assignments”
