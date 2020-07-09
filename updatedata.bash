# wget "https://open.canada.ca/data/api/action/package_show?id=90fed587-1364-4f33-a9ee-208181dc0b97" -c -O out.json
cat out.json  | jq ".result.resources[].url" | grep EN  | xargs wget -c
sed -i 1d *.csv
