#将英文地名和州首府 做对应翻译，漂亮打印！
#技能包：pyperclip（）；字典 列表方法 ；zip 并行遍历

ew = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
	'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
	'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
	'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois':
	'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas':
	'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine':
	'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan':
	'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri':
	'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada':
	'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
	'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
	'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
	'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee':
	'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':
	'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

	
cw_old ='''
	'阿拉巴马'：'蒙哥马利'，'阿拉斯加'：'朱诺'，'亚利桑那州'：'凤凰'，
	'阿肯色州'：'小石城'，'加州'：'萨克拉门托'，'科罗拉多'：'丹佛'，
	'康涅狄格'：'哈特福德'，'特拉华'：'多佛'，'佛罗里达'：'塔拉哈西'，
	'格鲁吉亚'：'亚特兰大'，'夏威夷'：'火奴鲁鲁'，'爱达荷'：'博伊西'，
	'伊利诺伊'：'斯普林菲尔德'，'印第安纳'：'印第安纳波利斯'，'爱荷华'：'得梅因'，
	'堪萨斯'：'托皮卡'，'肯塔基'：'法兰克福'，'路易斯安那州'：'巴吞鲁日'，
	'缅因州'：'奥古斯塔'，'马里兰'：'安纳波利斯'，'马萨诸塞州'：'波士顿'，
	'密歇根州'：'兰辛'，'明尼苏达'：'圣保罗'，'密西西比'：'杰克逊'，
	'密苏里州'：'杰斐逊城'，'蒙大拿'：'海伦娜'，'内布拉斯加州'：'林肯'，
	'内华达州'：'新罕布什尔州'：'康科德'，'新泽西'：'特伦顿'，'新墨西哥'：'圣达菲'，
	'纽约'：'奥尔巴尼'，'北卡罗来纳州'：'罗利' ，
	'北达科他'：'俾斯麦'，'俄亥俄'：'哥伦布'，'俄克拉何马州'：'俄克拉何马城'，
	'俄勒冈'：'塞勒姆'，'宾夕法尼亚州':'哈里斯堡'，'罗德岛'：'普罗维登斯'，
	'南卡罗来纳州'：'哥伦比亚'，'南达科他州':'皮埃尔'，
	'田纳西州'：'纳什维尔'，'德克萨斯'：'奥斯汀'，'犹他州'：'盐湖城'，
	'佛蒙特州'：'蒙彼利埃'，'弗吉尼亚'：'里士满'，'华盛顿'：'奥林匹亚'，
	'西弗吉尼亚'：'查尔斯顿'，'威斯康星'：'麦迪逊'，'怀俄明'：'夏延'
	'''


cw={'阿拉巴马':'蒙哥马利','阿拉斯加':'朱诺','亚利桑那州':'凤凰',
	'阿肯色州':'小石城','加州':'萨克拉门托','科罗拉多':'丹佛',
	'康涅狄格':'哈特福德','特拉华':'多佛','佛罗里达':'塔拉哈西',
	'格鲁吉亚':'亚特兰大','夏威夷':'火奴鲁鲁','爱达荷':'博伊西',
	'伊利诺伊':'斯普林菲尔德','印第安纳':'印第安纳波利斯','爱荷华':'得梅因',
	'堪萨斯':'托皮卡','肯塔基':'法兰克福','路易斯安那州':'巴吞鲁日',
	'缅因州':'奥古斯塔','马里兰':'安纳波利斯','马萨诸塞州':'波士顿',
	'密歇根州':'兰辛','明尼苏达':'圣保罗','密西西比':'杰克逊',
	'密苏里州':'杰斐逊城','蒙大拿':'海伦娜','内布拉斯加州':'林肯',
	'内华达州':'卡森市','新罕布什尔州':'康科德','新泽西':'特伦顿','新墨西哥':'圣达菲',
	'纽约':'奥尔巴尼','北卡罗来纳州':'罗利' ,
	'北达科他':'俾斯麦','俄亥俄':'哥伦布','俄克拉何马州':'俄克拉何马城',
	'俄勒冈':'塞勒姆','宾夕法尼亚州':'哈里斯堡','罗德岛':'普罗维登斯',
	'南卡罗来纳州':'哥伦比亚','南达科他州':'皮埃尔',
	'田纳西州':'纳什维尔','德克萨斯':'奥斯汀','犹他州':'盐湖城',
	'佛蒙特州':'蒙彼利埃','弗吉尼亚':'里士满','华盛顿':'奥林匹亚',
	'西弗吉尼亚':'查尔斯顿','威斯康星':'麦迪逊','怀俄明':'夏延'}

#制造规矩的的字典(包括冒号和逗号的替换)，复制到剪贴板粘贴再加上大括号组装成新的字典
import pyperclip   
replace_cw1 = cw_old.replace('：',':') 
replace_cw2 = replace_cw1.replace('，',',') 
a= pyperclip.copy(replace_cw2)
b= pyperclip.paste()

# 字典中分别取出键和值各自存为有序的列表,等待重组
ew_keys = list(ew.keys()) 
ew_values = list(ew.values())
cw_keys = list(cw.keys())
cw_values = list(cw.values())

# 格式模式 : 'Alabama'阿拉巴马: 'Montgomery'蒙哥马利

print ('*'*61)	
# zip函数：并行遍历 
for a,b,c,d in zip(ew_keys,cw_keys,ew_values,cw_values):  
	print ("{:<14}{:>8}{}{:<15}{:>8}".format(a,b,' '*(12-len(b)),c,d) )
print ('*'*61)
		
		
		
#此处有彩蛋 思路手稿Script
"""
todo：
让两个列表中的键和键对应起来，值和值对应起来
连接成这样：
	'Alabama'阿拉巴马: 'Montgomery'蒙哥马利
	
'Alabama': 'Montgomery'
	'阿拉巴马'：'蒙哥马利

how：
字典转换成列表--产生顺序 能一一对应
遍历两个列表 对应位置拼接起来

"""

		
		
		
		
		
		
		
		
		
		
		
		
