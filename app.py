import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))



import streamlit as st
import webbrowser
from utils.resume_parser import parse_resume
from utils.interview_prep import generate_interview_questions

from utils.career_journal import save_journal_entry, view_journal_entries

from utils.skill_gap import analyze_skill_gap
from utils.career_info import fetch_career_information
from utils.career_suggestor import suggest_career_ai
from utils.gcp_utils import upload_to_gcs

# WEBSITE CONFIGURATION
st.set_page_config(
    page_title="My Career Journal",
    page_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPIAAADQCAMAAAAK0syrAAABv1BMVEX8+c4AAADK6/z/762Q2/iR6PKp+frK7PjhZ5rkZZr8+dD+8a38+c35+8z5+s/hZ5byjLT//9j8ttiO3PmP2/mHzt+w/f89TFBvmpbwnL3M6/Z9fWhAPzD/+7XH7fjL6/yW3O//9qzL8viY2fqXk23V9f/yi7j89LtXdXl+QlX/9bPoZph/jpCR7POGhnIUCQyMSmN8n6Kf3d4hIyUdKSo7VVyqqZPhgqeBvr8cGB9JWl5JKTLLfZydmoLYZpTRZZFuNUspHCIABwCEwMyQR2VxfIKrT3E0GCMmDxakbIJFRDJdM0DMW4fb17i6WYGoWHcyMSq61NtkkaA0QEZQMD16rMLDcpGkoH3IxIrp6cbHxqi8tZzUybDX17ZtbGNWVUwaGRRCGCZbNEZiKju+V3qkWXY2JijJbZOYU2uBSGCemI2OioOfusGQpa9ZZ2gMFxlSeoYOHhyjwMMwEB2i1NiEutJZjJB4sas8O0IdLjKr5OsnJh9IamXAkqberchMPUSef4x9YnKy+vH/w91DTkrHkKpNaHVfnJhoTlY3RlKdb35hVV2ZZnron7l8V12O1uQrSUUfNTFzcle0r3nU0JG+CtXcAAAYhElEQVR4nO2djV8TV9bHOTE0LyQZMAEqdUOABwFHDBIQITQQjCAbTASCrdr6EgVJWwG3RRfairtaVvex1T7bP/g559w7k5mQhCAydD+f+bWSZGYyud859+WcO/feqauzZcuWLVu2bNmyZcuWLVu2bNmyZcuWLVu2bNmyZcuWLVu2bNmyZcuWLVu2bNmy9d8nrzfgZ/m83jqfz1cnXlABlBd34188LvChEiej8/rwV/CEx02MKfHqafKKz3IPXwefz39I+fTfoUv5J0D2lqiJ/wgFAuKlqUnbclDhGQL8XeNPHA+oT/w2mtAX4PRQsm7evHnt2le3bt26Tbqo63P8X+q8QZ/tUXGfPFx8n85266uv8fTMzlkH85TFyAEqv4EAMt66eP7bO3dP3wNrdO/unfMXv0Z2r89qZH+g6db5u9cPmuKoSaPJ5MzMTDwez+XSDx48SEvdv5+M7nOeuxebfBYzB/xfxUpSMQVXk/FcfnKykEqtpqZRGdQEK1FOihv/87gVRfF4PG58dQvRBkVJTGQy09nUwECqr29yMp2Oz8xcNV6IO01W8mI5aroof/lB38ByNpOZm0hg6t1uVVXpj+JWPW7i8FSRW5f8VNyFxApJlaIz80ETmYfTqb5J+uXb1FJYxhy4dhp/M519BDBHCSG7uCVGMe06TS3I5mMVFWmLx/CG4rVRE1E2s4XIPv9duswDqgow4UEjIPJECvPgavYhazqVWk64D4WcyC6nBjBHP8jn85N9hSwWA/0iKhmIJgFuWofs9d8EmJmBuDIB4FZEDlwprWAGFE9CK5tFaxEOfxJfK4vMex+VnG6Vyw0XeUVdhkIB4JrPslrbG7gFMHkDIIXICa3OmcgIzUnJnIlSKetTYeRiSRtURapYVOV7ugriTWaalZ0WZ1UNUtIwkcLC7LeuoQpg3ZXyZAFyAJmJuTmtCha1s0SfXl7GvMkaKBQGqNqdTOfT+XzuPjZMyaLw0/00N1D5dHpSVx+qUCiIM6QKVG6ECoU05OjXv/Fb540EvgEoeNQBbpmORVlC/tZK5G+p7lIUaivOfffdY9KFC+cq6vG5CybpO65c6V1bGxtrXdwaiq1XwltfX49JrcuDCm5lDqtsf13AMuTzWJaxzE2kAS50hl0uh8Ph6sYXeiNFG3FbdxjlcoVNcrl4C/6h/zvDnd0H0TysJNTEsSB7EurEFCxsM8FetbW1Fd+R2tvb5dsyR4fpP5SDLlt7O14zw+VxOdr5r4P/fgdxd8KdQKfTKmSKmhA5rlKjkYMFp6M97DiM2h3t+x4iRczhx/CAGiyA601ev1XIgc+xXaamxz0JG4js2i/JH02I3H0FJgXyj1YiYyM1w87QAAw7Iy5rkdfQy8EMFoV7ViGT94XISfacUrAYjITbrER2vYIs+nNqFKasQ67z38aGYo68p2mIRZxcgVmH/ASmyW/DyMJK5FsacgbWnWhmK5Hn0eM7BuRrGjK2jptBp8NK5L9h9GY9cuAm+XwacigUaS9facs2l95xk1uictv2R34MUY68Ro8LOQpLzpDTUb4CK++jVFRtyOfge0K23Mr3JHIiib4ImrkKcnd3jcTdNTDjUWOQ91iO7A14r2NcwaH8ffRFsAIrbyL0LLvnH1PcUFFjRa1dmO8MVygiUuh3dk9hEEcdDVYj36XoUSDvOoNUZ5dPY9uVA8WEV9rQqa7ifuKuNrrYx4F8B+MKRk7DcCQSQg+sbELnYwBDvZ9Wlowm+V3vEEBsvrMaMkLPU7AskGNWluUmRM67BfLvkWAXtlNlbbwF8OknLbXpk5ZPngGMtoWrIbe3fwfwiJHZx7YqePQFAp8hMne/TcIUAlPTXJo6lwMDAPjhn5/UrpYfpmCtu5qR2xyPAbivDYPH6wErkSl65D7JAfJFQlia9yKHMQ9e6G85APInn6Cf8V1VZNcVSHo0ZCut7KPokX5YXWXkUDC0J3WuznOw2F9/MOSWMbhSrcoOd7dCTqVe1QmAV1Za2Yeh1FSCOp6nAZaCQacztO0qbZu7F+Fpff3BzNzyDP5ezSsJh/9O/TEC+W7Aso4gX6COQilGzgAshAg5sqdvo20ILtXX1x/MyoMAbZWRXeG2GKQYec7CjiBGplBqgm4eYJHawNoLtTd9MUY+kJn3Q3Zg/TDNZdna7j5/wPuVhuwGGGbkPWZ2SeQDMUvkSvm6PYz1W4bv+GUI2bqyXOel6DFDGds9A1tkY4wtSjwwA7Jg5saXXzU++W8PciViRP6ObvwpAvlbC5G9jDyNyIp7EkBk7GCkJBNqyLqZWwYvXfpBByb0Hy5d2m45EPI5SCb4dt20xcg+CqUYmRrmCCFj02zO2UUr9wucwVb2o38alEa/LD73HgCZvJsZhe+uW4tch8g/ils0HncK4HKIkENdEfPtik7NyqLW3savJJME+Sk5l9s/0VsaE/JTixm5SrdSe+caPHBTu0z3pD63FJmixz5GpoaZ8zVWYKbSbESux1zcC/DzyZPPX2D+WMML8DvAzs/Pnz9/AfCs5hq7PfwK+gRyymrkJkLm4RLoEixwWcasvd1WCbmeWGYbT6Je/gMz8z8x4HjxUn5sbakV2RGOwaqHvS+LkX11TacxrlATHkUl5JBEjrgMySXky/068yVY+fXUKYI8+W/0FQF+OSn0HGCwZmSMlrN8Z8jTB3DRwlvqPm/TXborpRDy97DrFMJ4qhJyf/2/4PWpU6d+ZcodLMUvJPHJl1H4oaVWZOrR5TtDhGzlKAK08h26K+WmgTpxeBMJ6cxVkH87RZKGTb7UkVdg8CDICZU8IIxaCdmyLoI6bxMGzFFVobEqD2DLgNxWCfkZW1nY+eUO/OPky6KVa0dGT4RrELcnDXDLuuExdV5vE0aPIEbmTdI9Gokc6ir21onqS2e+BDunTml2fv7zSV3PYaj2GvsCI9PtsAeI7LVu6KpXDO7DLIY/j4WqWUc2tFNm5Pr+LfilyPyyiPwCek019np15BU5dCoOcM165DlGXpW+CBGHIkWv04TcH+l/ppv51EmDno8a8nUNyDvHg4wVGAXMGRpkSG6QRGY5ivdkTI1UfX0r/LsM8//CU7P3Fa2ETL3756hj1UPDxu4D3LR0rK6PAuaMh653Rm+YZXBRCXlwHcY15l+1uusFvDJ2CO6D7DoHA26BPGM1ct3XPPiKkB/q7pcWQ1ZAxhoMfj5VNPRLJh7aLgkropV8bDrvFUgJ5IT1yHQjblmVVt4IGs2sJbkbkevrS5jf6sy/IvVrIjZGjy3bMFotYyOyGMaZSPKwVQuJfYS8ysgTUdgtIqO9wzKI3Ivcf+kJ7PyiQ/+ShPeDJZ1jgzBaxcoYSGnIVyFq4UhdQvYCRY/coXwVhp0hQ86OVEbuHxwGrRL79TeAp/39WnDZUgtyt448F4WYtch1TUChFN+jScKiUy/MoeI9uT3ITP3sCayMY4AxC7B4ybSLuFtqRp46FuS8GEQ9A+vvnObS3M4pHDJXXxr0U4DfftmBoWclO0Q+gNFK/dhmZIDrNBzLSuTrBmR4Fwoas/Y2DYhwdZdFRqx3vdQ1UnZX/yDEarMyBqBWI1P0KOZR5NDjDBqQqaFqJ+StssiENqgV4r17ake+azFyHUWP3KFMDn5zyECMyF2OcLuruxUulAcje1bYcQlaK/bbi0aKu5LVjPXIdO8xqTAyRq6Xu4zIVJzbuQO2txJZJWFBv1Lp/vJxI/sxeowmeOoEhlJLXUEzstMR5nh+8IDIg09gvgpyWEPmmxVN1iPDHHeiDxCy2cohjiJda/C+ai6ur+8v+dQLaxVHEQgr94mpWFnrkb0XNWT3KsUVZmSOnNtcbTFoHRTA+Le/Cjof0d+/C9C2dzzCHmRVURH5M4uRm27pyMvlkJ1OtHOYhsf89PTSYH1/JVNjsyQuxeDgu4UhGJqvfKtCIE8K5JT1yOJGHE/kyppCKQ05FAy3tTvm1+SUkK3f37e2tj7dk5WfDj0Z2toaGhp6QjNF1uZd7e3VM3YR+bzFyL5rHErRMDsKmIMlViZFaNxaeP7xubHFoXtyTuqwKXtT2f1xbay1dXFxcWtx7ByauMoQAoGco3ZZ9NxbOeeRRKFUipEfmqNHQ/NMo1Ud4c5wZ2dnOBxua5vfQub6SBF5DGLz3TTmsbuzu9vlaNsPuVMgY/3VZz2yl5D7CJkmPm5E9hIHQ8HIdtjVrks0W8PbxRbpPUTnw9oEG5RDmylTCRkbqThZmZEvWjqZl3r80Mme5FmNCYDe0rLMyFiiI9Q+y2GpNGmImPu5QPfXD/6ONi4Zv1htmJtAnmFk7rm3eB0Gr/cVQNojx9n1OstkbK63u3jwqma5MI0CGBaZejAG6/OVxn5WRk6qPKudeu7rLGYOYFyR4xpbpeEiFRTi9tmA7ELm99RkXVpn4g9EdhOyxctt+AJ3xMQhRF6H95WQg8FgJFJExpduZH7VX3+BhqhijfahyNyNbbWV6a4U3ehV3DMQC4bKlGYNG6EN0/66H6OdMWIeqnbvaT9kBZG/tnqVDXayGdmTB4h0VUamWmwb2+gw3312hTsfUwu9OH/QSSgm5BlEtpi4jqaH0dAvt6Ii8rtqyCHqEMO628WWdoS7/7a4da6tWhNcBXmFkRNXqRvbYmLvLZjiCUuKWqBpNJWJRZnGP0hNTqjDgY4JNsBtss2W5DXMvtBcEYUaxqnjQAaelqaIAcrVkaUikQh5YWFRsGnSkJitWiMxWfkBO5yIfM/qFXMCfIsmxTd7ebTu/ryUv+m1qwu50Q11OTiEEF5KjcitIqygQTk/NlmM7GMne0BDXgjRrdYgKUTiIdrUb2DsBaR94p2THNSuCN+aDcsZYuGwS3JrE7XNtLStOwZ9XGNO0AB0q5G93hi5XzSmUQ5QXtro3WVtbOzu9vYuLL2LOEvj6BKza3sjNWo7SnceERl/8rTlyAHqyc4RMl3yDUTe3Nh9Y1oqaWuzOrKTXVKRLULktfDQC/7U1SVeTQqGIgCr/JOYse5aj0we5wz/fiIKuyGaYIFpbnY2k5w0liJCmTkUrIgd1BUqc4wZV2xrpvHBHoF8x/qyTAsSRBXpFwzL/NkVad5cWlowaGlpqZnLcVd1e9egYHCThiaTj4uNxLdWr+qGyDzZgMZxKjl4w6PQnbuj5We5te4uLB2amKoLSHJHshuRv7H0TgUjc8M8QYv6qGlYjDDy5sabRdTvvw8NPXmyvj4l9OTJ0NbiWC3t2D7IkQURvHloEZeLlrvYPu4XyahYtDCbLVKaIuRXRuojonwWi2pXF3lfQXPZDMk2LWjeLjeHiruLBd7p3BDTDt1u9HFvW0xMyHS/tZCZ4BUJRpspiVTREh/aw1liU7wWps94capZPRjcuxe/0sptlDtBUcUtq8syIfNahdGZeA4jud6NC7K+uoA11ubmppbycipnw0oqNsrOSDN1qvJCWVEe9WWhsBQF0BfZd27u+tZi69jYWm8ZrWnSZi8bJzUvLr5//35xcYs1xIrFYlut6/oKj1MYSFlK7Ke1ZK+9IqpjWvwKZW23PVqYm6h4Vqzopi1vRgubTU/zmmZ9k/l8Oj5z9ep+C2p+sKz1RLxevgtXUFRaTDPBa9kpvPZe2YX43Hg95ubmMpksrUy3uroql2frM6lQKJg+i7XdHsg13h6w0rlcnDRqqZUpV/t41OpAgkcR6IvuacvxiaUUDesv0np9ipjdJC6EXNVPrlhIG8TyhcbFLN3Fd5oUWuSPTk2LfcEdr1Wduj5t3dGCsCsPqDQZVaU1NAk9QUumUnZ/lMCjprPZrLasX6kyGUUVixcq5aVdVXEVlAT62PBtwG/RSF05MnkgoQpQRQAm5uYo+yIPLZ+Zz8WNvud9JRHfp2guq8pAPD6jixbapXV2Jw3qeyQzD3c+wcUmC5DJxDJXq6LAuj1qZjKeTF4VLUd5ff+IpnZX14yi7HdVAK4+8nDORmekD8Sw+6PuDkIHxMdzDLIeWVepyrI5VfdiW1tvhnd7ezfIL9nYGMbGNOsmd+lyc0VdXiQzpwF22ZvZ2JXN9Js3b4Z17bZis5zxyIkGCvqctPjoUSOjkWkoUDSratWzSsTRxeGxjQX2upp1x1K4TsHIOiS57O2WhsBFdQUXsMVTxI1qDo7xq0W/U3pgwcgu/tRcQoy6V4j53s0jXxlcLNs3lfEkJLKSReKFZpG6EHeACVdSOptOjPcg5VbJyJEqbuU7oOA/D8NB6hXUL5l+5djhDEbe0B0SVVSXSmKFV2A4QmT2ufxk4zmVV7Sm5aAfAjzZJFgtCuAZnxoc2WuXIsxlnthdxZEOblCvEuaFy+JE3Buq+eN8AaiPyBmJUW4QIbObOqB48NeRUXPV9Q0STyhyEW8PjcvZukyYXV2yg5M7QPSAED/HIO+m6nqpTH7W5XRuAi3jFYWnYmik1lEqqKmTSbxv3sJLI5HdHm6qjvSpDtw6RbOKqiFj4Zva1GId6gFCbTYjQTH8WaKqDo+LbVauvJqb37179x5gEiP/dWeEvi3ORRHZktTC0gK/AC8BKkqVm5qq24EjQ5btcVbV1kr2uHOikh6tvDgs1W2P1Ml9Wx+hiYc1HieGyCieBFbyR3Vvih7HIXwugxtYG0qfmqiROJkwNs1Xr2JrbxZ7KOnJAb7hyf7poyh5nkfCjMh+uiOzIiZZivgJvRDhL/KC0OZQYZIiqfT99ORqQklgJJEa0Bd71kVfm54mN5ROsTo94fFoS01PkLOaoPXuzQ8EUDyq9DrJq1U9E3SNrh0FsbbeKKz0pTA5nKvd3O1VXeiIUgxR+QCP+OeRa4V72IlV9cXE3WUkFlen4Gy5T2SKz+uOwsz09BvtGQYQjcfzJt/XJLIxmnB1dXk5iybEkAHjCQobs0Li2Q4PH7I18TMG1wOG+FBGiWlaJBz/j+dkvGjSzIzxwRZH8zgHDfnIAv4PVDK3Q/7IESK/bRy/cWP2bSGfT0J0hSQXbx/FqIKSEBPbakhsNCq/Kk+0Iuy3EkUMzZijMFU+VEnG04W3szdGGhsb3+LHI0H2iiZq/AwLfykPhcbGEbPGAW408la8MDcevYWV8fFH42YBjIwbvnJmZBlWGo3agVn9fR5m9XMLjYw8Gr9BCzk0ypScKRw1cqOGnCPkEo0IZE2zkMOUlRwDYNp2pvGGGflM0oD82vC+eMRIFGbPaMiNaZo9dITIIzpyfF/kM2/LIk81nqmKPArL2q7GApYkbbuev840JmG1iJyjhvnjMYsnn4mHZPloWbMR+bON+LNvG/eoLLKZEEbPmDfMIrJMPf/FwPmMpgLk6etnSpRDZPGVkRuzSVpsg/pc6dFWPv9hmyt/wEsPd/P5fD1nOzq+ANjBstUokffmOcxx48Xy/etvhGzcPTJyahbiI8YqYHzkLSR/EeX0xg2qGwF+G59FvUXlsDbAWuHGrFk78Jr2v5YPRLnXc7anp4cfoIaV7GGtTPL39DR0NDR0dPxHNgu5/E4es9PO69ev8+hi5XbiVG/LR2iZatjkb3lSDg8YjWq7SuvgQ3f+3z6LyUP19PAD+Q4nL/KieU+wGjq+rHD3+CMm/+C6/uXZBkqdpPYdghmLhbeuh08kkdHSX/z1IyZ2auoe60fSdV2nT5+mf0X9Vciw5brc/n+ff/HHX6RFJHRDz4f3DGG15cMMc0JHZua//PHlF/9TSV/o+o/Ql0X9UUEnTmA57DnbcLaM/lJJ2s6Ojg4tcTpyR8+HI3u9PaKMFM96Akt1eTWYd+xNPjL1sE7gB3nUieK7Bk1a+k0YxXfFg/DlbPFA/YgTHQ0fXGljtj5L17DhhMHQWrk2Jch4Tfbs0g7Yk+SSw0+UfqGaipfBvJFS23D2g9cN8vmRmYzXcGLfJPwpRKmkpuUQGdvvbcL2qaOjhqv+pxCn82zPIdopLz8Q1ktOiKnW/rPRG5N2toeen3rYBbHQ9aIaVVRR2qlrKnBHLFNFJnh7yMCH7yDxB4SDTQ1JQ0k1c9y81CTxP/Y3P9rdZj8x+7h73C9c7QZukP4cxGep6eMnQNNTnj/aEm/kk2hPVxZPQO7BXyrbQlXPAOY9+2YW816toROfRCNPedjwfOIjmA3o1ZjrmkR0RYUcnQzhAu1J4R6ahgqqzipyFP2I8NB65DO3vcYnP390VhMy9YL5OUAtytejq8hRifCAkuf1aYBNMhGmx1wfFbIEp5hUzCkVzwzXf5cfmO6t46eM9xhl9jyL0l1RKdOX2JrF3/TzQ9X9YhO++sVj1o/9GeN1ex8zLup7Y56ocGyd+SiLDPgx5NXbRhNvQDwIPlBG8hnxgVLI/xpkyYCgZjCZfmFNrQYymtdwrNgrPxw3kC1btmzZsmXLli1btmzZsmXLli1btmzZsmXLli1bH6D/Bxvo4GtKyESDAAAAAElFTkSuQmCC",
    layout="wide")
st.title("My Career Journal")
def pretty_divider(height="8px", color="#f87171", radius="6px", gradient=False):
    if gradient:
        bg = f"linear-gradient(90deg, {color}, #ffb3b3)"
    else:
        bg = color
    st.markdown(
        f'<div style="height:{height}; background:{bg}; border-radius:{radius}; margin:18px 0;"></div>',
        unsafe_allow_html=True
    )
pretty_divider(gradient=True)

# CSS STYLING
st.markdown(
    """
    <style>
     /* SETTING BG AS IMAGE */
    .stApp{
        background-image: url("https://img.freepik.com/premium-photo/notebook-cup-coffee-with-beautiful-pattern-notepad-pink-background-place-text_96727-2494.jpg");
        background-size: 100% auto;       /* cover the whole screen */
        background-position: center;  /* center the image */
        background-repeat: no-repeat;
        background-attachment: fixed; /* keeps image fixed on scroll */
    }

    /* TO ENHANCE TEXT */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-color: rgba(255, 255, 255, 0.5); /* adjust opacity */
        z-index: -1;
    }
    h1, h2, h3, h4 { color: #f87171; }
    div.stButton > button { background-color: #f87171; color: #fff; border-radius: 8px; border: none; }
    div.stButton > button:hover { background-color: #ff4f4f; color: #fff; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #fff7d1; color: #000; }
    .streamlit-expanderHeader { color: #f87171; }
    .stTabs [role="tablist"] { background-color: #ffe486 !important; border-radius: 8px; padding: 5px; margin-bottom: 10px; }
    .stTabs [role="tab"] { color: #f87171; font-weight: bold; border-radius: 8px; }
    .stTabs [role="tab"][aria-selected="true"] { background-color: #f87171 !important; color: white !important; }
    [data-testid="stSidebar"] { background-color: #ffe486; color: #f87171; }
    .stAlert > div { color: #333 !important; font-weight: bold; }
    hr {
        border: none;
        height: 6px;  /* thickness */
        background-color: #f87171;  /* your color */
        border-radius: 3px; /* optional, makes edges rounded */
    }
    </style>
    """,
    unsafe_allow_html=True
)






# SETTING RESUME PARSER AS DEFAULT PAGE
if "resume_skills" not in st.session_state:
    st.session_state["resume_skills"] = []

# SETTING THE NAVIGATION BAR "MAIN MENU"
st.sidebar.image("https://cdn.dribbble.com/userupload/23015496/file/original-32e6a015bc2cb77eeb9e8f13f54a1000.gif", use_container_width=True)

sidebar_option = st.sidebar.selectbox(
    "Navigate",
    ["Career Suggestor", "Career Developer", "Career Tracker"]
)

# CAREER TRACKER CODE
if sidebar_option == "Career Tracker":
    st.header("My Journal")
    entry = st.text_area("Today’s reflection...[date:reflection]", key="journal_textarea")
    if st.button("Save Entry", key="save_journal"):
        if entry.strip():
            save_journal_entry(entry)
            st.success("Entry saved !")
    if st.button("View Past Entries", key="view_journal"):
        entries = view_journal_entries()
        st.subheader("Previous Entries")
        for e in entries:
            st.write(f"- {e}")

# CAREER SUGGESTOR
elif sidebar_option == "Career Suggestor":
    st.header("Career Suggestor")

    # TAKING SKILLS AS INPUT
    skills_input = st.text_area(
        "Enter your skills",
        value=", ".join(st.session_state.get("resume_skills", [])),
        key="career_suggestor_skills"
    )

    # TAKING APTITUDE AS INPUT
    aptitude_score_input = st.text_input(
        "Enter your aptitude score (0–100)",
        key="career_suggestor_aptitude"
    )


    try:
        aptitude_score = int(aptitude_score_input) if aptitude_score_input else 0
    except ValueError:
        st.error("Please enter a valid number for aptitude score.")
        aptitude_score = 0

    # SETTING TEST LINK IF APTITUDE NOT GIVEN
    st.write("Don’t know your aptitude score? Take a free test:")

    # This is an actual button, not markdown
    if st.button("Take Free Aptitude Test", key="aptitude_test_button"):
        webbrowser.open_new_tab("https://aptitude-test.com/")
    # SUGGEST CAREER BUTTON
    if st.button("Suggest Careers", key="suggest_careers"):
        suggestions = suggest_career_ai(skills_input, aptitude_score)
        st.subheader("Suggested Careers:")
        for career in suggestions:
            st.write(f"- {career}")


# CREATING CAREER DEVELOPER MENU
else:
    tabs = st.tabs(["Resume Analyzer", "Interview Prep", "Skill Gap Analysis", "Career Information"])

    # RESUME ANALYSER
    with tabs[0]:
        st.header("Resume Analyzer :heart:")
        uploaded_file = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"], key="resume_upload")
        if uploaded_file:
            st.info("Uploading your resume...")
            gcs_path = upload_to_gcs("careerbucket25", uploaded_file, uploaded_file.name)
            st.success("Uploaded to Google Cloud")

            st.info("Analyzing your resume...")
            result = parse_resume(uploaded_file)
            if "error" in result:
                st.error(f"Error parsing resume: {result['error']}")
            else:
                st.subheader("Extracted Fields")
                for key, value in result.get("entities", {}).items():
                    st.write(f"**{key.capitalize()}**: {value}")
                if "skills" in result.get("entities", {}):
                    st.session_state["resume_skills"] = result["entities"]["skills"]
                    st.info(f"Skills saved: {', '.join(st.session_state['resume_skills'])}")

    # INTERVIEW PREP
    with tabs[1]:
        st.header("Interview Preparation")
        job_role = st.text_input("Enter the job role", key="interview_job_role")
        if st.button("Generate Questions", key="generate_questions") and job_role:
            questions = generate_interview_questions(job_role)
            st.subheader("Practice Questions")
            for q in questions:
                st.write(f"- {q}")

    # SKILL GAP ANALYSIS
    with tabs[2]:
        st.header("Skill Gap Analysis")
        skills = st.text_area(
            "Enter your current skills (comma separated)",
            value=", ".join(st.session_state.get("resume_skills", [])),
            key="skill_gap_skills"
        )
        target_role = st.text_input("Enter your target role", key="skill_gap_target_role")
        if st.button("Analyze", key="analyze_skills") and skills.strip() and target_role.strip():
            table_md = analyze_skill_gap(skills, target_role)
            st.subheader("Skill Gaps")
            if table_md:
                st.markdown(table_md, unsafe_allow_html=False)
            else:
                st.write("No major gaps detected")

    # CAREER INFORMATION
    with tabs[3]:
        st.header("Career Information")
        career_role = st.text_input("Enter your dream career (e.g., Quant Research Analyst)", key="career_info_role")
        if st.button("Get Career Info", key="get_career_info"):
            fetch_career_information(career_role)




