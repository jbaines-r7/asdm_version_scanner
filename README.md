# ASDM Version Scanner

The ASDM Version Scanner will load a CSV of IP addresses and ports and attempt to connect to `/admin/public/index.html` via HTTPS. Once successfully connected, the script will then attempt to extract the ASDM version number from the page's `<title>`. I use the script like so:

## Step 1: Download potential targets from Shodan

```
shodan download --limit -1 title_cisco_asdm title:"Cisco\ ASDM"
shodan download --limit -1 default_ssl ssl:"ASA\ Temporary\ Self\ Signed\ Certificate"
shodan download --limit -1 webvpn_cookie "Set-Cookie: webvpn_portal"
```

## Step 2: Extract the IP and ports into csv files

```
shodan parse --fields ip_str,port --separator , title_cisco_asdm.json.gz > title.csv
shodan parse --fields ip_str,port --separator , default_ssl.json.gz > default.csv
shodan parse --fields ip_str,port --separator , webvpn_cookie.json.gz > webvpn.csv
```

## Step 3: Remove duplicates

```
cat title.csv > all.csv
cat default.csv >> all.csv
cat webvpn.csv >> all.csv
cat all.csv | sort | uniq > all_uniq.csv
wc -l all_uniq.csv
$ 212874 all_uniq.csv
```

## Step 4: Begin scanning

```
python3 asdm_version_scanner.py --csv ./data/06152022.csv > ./output/06152022.txt
```

## Step 5: Sort and count the collected data

```
cat 06152022.txt | grep -oP 'Cisco ASDM \d\.\d.*$' | sort | uniq -c | sort -nr
   3202 Cisco ASDM 7.8(2)
   1698 Cisco ASDM 7.13(1)
   1597 Cisco ASDM 7.15(1)
   1139 Cisco ASDM 7.16(1)
   1070 Cisco ASDM 7.9(2)
   1009 Cisco ASDM 7.14(1)
    891 Cisco ASDM 7.8(1)
    868 Cisco ASDM 7.17(1)
    778 Cisco ASDM 7.6(1)
    756 Cisco ASDM 7.12(2)
    745 Cisco ASDM 7.12(1)
    520 Cisco ASDM 7.9(1)
    481 Cisco ASDM 7.10(1)
    297 Cisco ASDM 7.5(1)
    288 Cisco ASDM 7.7(1)
    140 Cisco ASDM 7.6(2)
    110 Cisco ASDM 7.5(2)
     64 Cisco ASDM 7.4(1)
     51 Cisco ASDM 7.18(1)
     46 Cisco ASDM 7.1(3)
     44 Cisco ASDM 7.2(2)
     18 Cisco ASDM 7.4(3)
      8 Cisco ASDM 7.4(2)
      7 Cisco ASDM 6.6(1)
      5 Cisco ASDM 7.3(1)
      3 Cisco ASDM 7.2(1)
      3 Cisco ASDM 7.1(6)
      3 Cisco ASDM 7.1(4)
      3 Cisco ASDM 7.1(1)
      2 Cisco ASDM 7.3(2)
      2 Cisco ASDM 7.1(2)
      1 Cisco ASDM 7.3(3)
      1 Cisco ASDM 7.1(5)
      1 Cisco ASDM 6.4(5)
```
