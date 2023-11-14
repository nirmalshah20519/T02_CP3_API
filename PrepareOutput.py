def format_output(y, team1, team2):
    output={}
    if y < 0.5:
        output['winner'] = team2
        output['winning_chances']=str('%.2f'%((1-y)*100))
    else:
        output['winner'] = team1
        output['winning_chances']=str('%.2f'%(y*100))
    return output