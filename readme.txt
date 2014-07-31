From ..
    appcfg.py --oauth2 update aspastats/

To fix wrong dates on data entry:
    SELECT * FROM Match where date > date(2014,5,10)

To select by season:
    SELECT * FROM PlayerSummary where season = KEY('Season', 'Sum14') and player = KEY('Player', 'KimM')
    