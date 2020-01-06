From - Thu May 13 16:33:13 1999
Return-Path: <John.Grayson@GSC.GTE.Com>
Received: from h2.mail.home.com ([24.2.2.28]) by mail.rdc1.ct.home.com
          (InterMail v4.00.03 201-229-104) with ESMTP
          id <19990513185621.UCFG9253.mail.rdc1.ct.home.com@h2.mail.home.com>
          for <johngrayson@mail.wwck1.ri.home.com>;
          Thu, 13 May 1999 11:56:21 -0700
Received: from mx1-e.mail.home.com (mx1-e.mail.home.com [24.2.2.29])
	by h2.mail.home.com (8.9.1/8.9.0) with ESMTP id LAA12051
	for <johngrayson@home.com>; Thu, 13 May 1999 11:56:20 -0700 (PDT)
Received: from Ballad.GSC.GTE.com (N192311198.GSC.GTE.Com [192.31.1.198])
	by mx1-e.mail.home.com (8.9.1/8.9.1) with ESMTP id LAA26599
	for <johngrayson@home.com>; Thu, 13 May 1999 11:56:19 -0700 (PDT)
Return-receipt-to: John.Grayson@GSC.GTE.Com
Received: from gscex02.gsc.gte.com ("port 2176"@[131.131.133.151])
 by Ballad.GSC.GTE.Com (PMDF V5.2-30 #29038)
 with ESMTP id <01JB5C0CAP8200125U@Ballad.GSC.GTE.Com> for
 johngrayson@home.com; Thu, 13 May 1999 11:56:04 -0700 (PDT)
Received: by GSCEX02 with Internet Mail Service (5.5.2448.0)
	id <KLWL3HK4>; Thu, 13 May 1999 14:55:55 -0400
Content-return: allowed
Date: Thu, 13 May 1999 14:55:35 -0400
From: "Grayson, John" <John.Grayson@GSC.GTE.Com>
To: "'jeg'" <johngrayson@home.com>
Message-id: <3774EF539472D211B98F0008C7F468A10119FF72@tntnex01.tntn.gtegsc.com>
MIME-version: 1.0
X-Mailer: Internet Mail Service (5.5.2448.0)
Content-type: multipart/mixed;	boundary="----_=_NextPart_000_01BE9D72.3AF267F0"
X-Mozilla-Status: 8001
X-Mozilla-Status2: 00800000
X-UIDL: <3774EF539472D211B98F0008C7F468A10119FF72@tntnex01.tntn.gtegsc.com>

This message is in MIME format. Since your mail reader does not understand
this format, some or all of this message may not be legible.

------_=_NextPart_000_01BE9D72.3AF267F0
Content-Type: text/plain;
	charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

 <<phone.py>>=20

<(=A9=BF=A9)>John Grayson
      John Grayson
GTE Government Systems
400 John Quincy Adams Road,
Taunton, MA 02780-1069


------_=_NextPart_000_01BE9D72.3AF267F0
Content-Type: application/octet-stream;
	name="phone.py"
Content-Disposition: attachment;
	filename="phone.py"

def get_phone(field):
    res = ''
    for idx in range(len(field)):
	if not field[idx] in '(),- ':          # NOTE: There is a space after the hyphen
	    res = res + field[idx]
    return (res)

def set_phone(field):
    res = field
    if len(field) == 10:
	res = '(%s) %s-%s' % (field[:3], field[3:6], field[6:])
    elif len(field) == 7:
	res = '%s-%s' % (field[:3], field[3:])
    return res

------_=_NextPart_000_01BE9D72.3AF267F0--
