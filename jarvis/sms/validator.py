
def validate_au_mobile(mobile):
    if not mobile:
        return ''
    mobile = mobile.strip()
    if mobile.startswith('+61'):
        mobile = mobile.replace('+61', '')
    if mobile.startswith('061'):
        mobile = mobile.replace('061', '')
    if mobile.startswith('0061'):
        mobile = mobile.replace('0061', '')
    if mobile.startswith('4'):
        mobile = '0' + mobile
    if mobile.startswith('04') and len(mobile) == len('0413725868'):
        return mobile
    return ''
