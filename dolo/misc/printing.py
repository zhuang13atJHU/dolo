from sympy.printing.str import StrPrinter


def sympy_to_dynare_string(sexpr):
    s = str(sexpr)
    s = s.replace("==","=")
    s = s.replace("**","^")
    return(s)


class DoloPrinter(StrPrinter):
    def _print_TSymbol(self,expr):
        return expr.__str__()

dp = DoloPrinter()



#############################################################################
# The following functions compute the HTML representation of common objects #
#############################################################################



def print_table( tab, col_names=None, row_names=None, header=False):
    #table_style = "background-color: #A8FFBE;"
    #td_style = "background-color: #F8FFBD; border: medium solid white; padding: 5px; text-align: right"
    txt_lines = ''
    for l in tab:
        txt_columns = ['\t\t<td>{0} </td>'.format(str(c)) for c in l]
        txt_columns = str.join('\n',txt_columns)
        txt_lines += '\t<tr>\n{0}\n</tr>\n'.format( txt_columns )
    txt = '<table>{0}</table>'.format(txt_lines)
    return txt

def print_array( obj,row_names=None,col_names=None):
    import numpy
    tab = numpy.atleast_2d( obj )
    resp = [[ "%.4f" %tab[i,j] for j in range(tab.shape[1]) ] for i in range(tab.shape[0]) ]
    if row_names:
        resp = [  [row_names[i]] + resp[i] for i in range(tab.shape[0]) ]
    if col_names:
        if row_names:
            resp = [[''] +col_names] + resp
        else:
            resp = [col_names] + resp
    return print_table(resp)

def print_model( model, print_residuals=True):
    from sympy import latex
    if print_residuals:
        from dolo.symbolic.model import compute_residuals
        res = compute_residuals(model)
    if 'equations_groups' in model:
        if print_residuals:
            eqs = [ ['', 'Equations','Residuals'] ]
        else:
            eqs = [ ['', 'Equations'] ]
        for groupname in model['equations_groups']:
            eqg = model['equations_groups']
            eqs.append( [ groupname ,''] )
            if print_residuals:
                eqs.extend([ ['','${}$'.format(latex(eq)),str(res[groupname][i])] for i,eq in enumerate(eqg[groupname]) ])
            else:
                eqs.extend([ ['','${}$'.format(latex(eq))] for eq in eqg[groupname] ])
        txt = print_table( eqs, header = True)
        return txt

    else:
        txt = print_table([['','Equations']] + [(i+1,model.equations[i]) for i in range(len(model.equations))], header=True)
    return txt

