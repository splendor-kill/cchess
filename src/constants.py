FULL_BOARD = '''
車－馬－象－士－將－士－象－馬－車
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－砲－＋－＋－＋－＋－＋－砲－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
卒－＋－卒－＋－卒－＋－卒－＋－卒
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
兵－＋－兵－＋－兵－＋－兵－＋－兵
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－炮－＋－＋－＋－＋－＋－炮－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
俥－傌－相－仕－帥－仕－相－傌－俥
'''

EMPTY_BOARD = '''
１　２　３　４　５　６　７　８　９
{p00}－{p01}－{p02}－{p03}－{p04}－{p05}－{p06}－{p07}－{p08}
｜　｜　｜　｜＼｜／｜　｜　｜　｜
{p10}－{p11}－{p12}－{p13}－{p14}－{p15}－{p16}－{p17}－{p18}
｜　｜　｜　｜／｜＼｜　｜　｜　｜
{p20}－{p21}－{p22}－{p23}－{p24}－{p25}－{p26}－{p27}－{p28}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p30}－{p31}－{p32}－{p33}－{p34}－{p35}－{p36}－{p37}－{p38}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p40}－{p41}－{p42}－{p43}－{p44}－{p45}－{p46}－{p47}－{p48}
{p50}－{p51}－{p52}－{p53}－{p54}－{p55}－{p56}－{p57}－{p58}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p60}－{p61}－{p62}－{p63}－{p64}－{p65}－{p66}－{p67}－{p68}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p70}－{p71}－{p72}－{p73}－{p74}－{p75}－{p76}－{p77}－{p78}
｜　｜　｜　｜＼｜／｜　｜　｜　｜
{p80}－{p81}－{p82}－{p83}－{p84}－{p85}－{p86}－{p87}－{p88}
｜　｜　｜　｜／｜＼｜　｜　｜　｜
{p90}－{p91}－{p92}－{p93}－{p94}－{p95}－{p96}－{p97}－{p98}
九　八　七　六　五　四　三　二　一
'''

well_known_1 = '''
＋－＋－象－士－將－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－士－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－＋－＋－象－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－傌－俥－俥
＋－＋－相－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－車－兵－＋－兵－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－卒－相－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－卒－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－＋－帥－＋－＋－＋－＋－＋
'''

well_known_2 = '''
＋－＋－＋－士－將－士－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－馬－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－卒－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
相－＋－＋－＋－＋－仕－＋－＋－相
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－帥－砲－卒－卒－卒
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－＋－仕－馬－車－車－砲－卒
'''

well_known_3 = '''
砲－＋－象－士－＋－將－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－俥－＋－＋－俥－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－＋－士－象－＋－＋－＋－傌
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－炮－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－卒－＋－卒－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－卒－＋－帥－＋－＋－＋－＋－＋
'''

well_known_4 = '''
＋－＋－象－士－將－馬－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－俥－士－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
馬－＋－＋－＋－象－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
卒－＋－卒－＋－＋－＋－卒－＋－卒
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－傌－車－＋－＋－＋－＋
＋－＋－＋－＋－＋－砲－車－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
兵－＋－傌－＋－＋－＋－＋－＋－兵
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－炮－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－仕－俥－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－相－＋－帥－仕－相－＋－＋
'''

well_known_5 = '''
＋－＋－象－士－將－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－士－馬－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－＋－＋－象－＋－砲－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－卒－＋－＋－＋－卒
｜　｜　｜　｜　｜　｜　｜　｜　｜
卒－＋－＋－馬－＋－＋－＋－＋－＋
＋－＋－兵－＋－砲－炮－兵－傌－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
兵－＋－＋－傌－＋－＋－＋－＋－兵
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－炮－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－仕－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－相－仕－帥－＋－相－＋－＋
'''

kaggle_1 = '''
＋－炮－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－將－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
象－＋－＋－＋－象－士－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
卒－＋－＋－＋－＋－＋－卒－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－卒－＋－＋－＋－＋－馬－俥
＋－＋－＋－＋－＋－＋－兵－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
兵－＋－＋－＋－＋－＋－＋－＋－兵
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－仕－車－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－＋－相－＋－帥－仕－相－砲－＋
'''
