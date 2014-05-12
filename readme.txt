From ..
    appcfg.py --oauth2 update aspastats/

To fix wrong dates on data entry:
    SELECT * FROM Match where date > date(2014,5,10)
