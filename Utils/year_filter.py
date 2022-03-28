import datetime
class year_filter(object):
    @classmethod
    def find_none_year(cls,pp_list):
        now_year=int(datetime.datetime.now().strftime('%Y'))
        
        none_indicator_name_year={}
        for pp in pp_list:
            indicator_name=pp.indicator_name
            year=int(pp.year)
            if not indicator_name in none_indicator_name_year:
                none_indicator_name_year[indicator_name]=[year]
            else:
                none_indicator_name_year[indicator_name].append(year)
        for none_indicator_name in none_indicator_name_year:
            none_list=none_indicator_name_year[none_indicator_name]
            min_year=min(none_list)
            max_year=max(none_list)
            abs_year_list=[]
            for year_ in range(min_year,max_year+1):
                abs_year_list.append(year_)

            none_year_list=set(abs_year_list).difference(none_list)
            none_indicator_name_year[none_indicator_name]=none_year_list
        return none_indicator_name_year

    @classmethod
    def year_sort(cls,info_dict):
        for indicator_name in info_dict:
            year_list=info_dict[indicator_name]
            year_list.sort(key=lambda k: k['year'])
            info_dict[indicator_name]=year_list
        return info_dict