redis-cli --scan --pattern amazon_products:* |\
grep -e "^amazon_products:[^:]*$"
awk '{print "hmget " $0 " rating productpagelink department manufacturer datescrapped countryoforigin picturereflink productname affiliatelink price"}' |\
redis-cli --csv > amazon_products.csv
