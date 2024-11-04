from flet import *
import json
import os

# مسار ملف JSON لحفظ البيانات
PRICE_FILE = "prices1data.json"

# البنود والأسعار الافتراضية
default_items = {
    "جليتر": 700,
    "برومو": 2200,
    "درون": 1000,
    "دي جي": 1500,
    "كلر": 800,
    "باندا": 600,
    "درامز": 1800,
    "استيدج": 1200,
    "باصات": 900,
    "كمان": 0,
    "ناي": 0,
    "ساكس": 0,
    "تنظيم": 150,
    "شماريخ": 300,
    "بالونات + اقلام": 500,
    "طبله": 0,
    "جيتار": 0,
    "كاميرا 360": 0,
    "رحله نيلية": 0,
    "العاب بامب": 1200,
    "مسرح": 0,
    "كورال": 0,
    "ارت": 0,
    "فقرات": 0,
}

default_items2 = {
    "فوم": 30,
    "وجبة": 80,
    "عصير/كنز": 15,
    "هودي /تيشرت": 180,
    "المكان": 30,
    "هدية": 5,
    "درع + وشاح": 0,
    "مسدس": 10,
}

# تحميل أو استعادة البيانات
def load_prices_from_file():
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE, "r") as f:
            data = json.load(f)  # قراءة البيانات مرة واحدة
            return data.get("items", default_items), data.get("items2", default_items2)  # استخدام get مع القيم الافتراضية
    return default_items, default_items2

# حفظ البيانات في ملف
def save_prices_to_file(items, items2):
    with open(PRICE_FILE, "w") as f:
        json.dump({"items": items, "items2": items2}, f)

fom=Checkbox(label="......", value=False)

items, items2 = load_prices_from_file()

def main(page: Page):
    global items, items2
    page.title = "Royal Team"
    page.scroll = "auto"
    page.theme_mode = ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 740
    page.padding = 0

    # حقل إدخال للمستخدم
    num_of_person = TextField(label="عدد الأفراد", icon=icons.PERSON_2_OUTLINED, rtl=True, width=150)

    # نص لعرض النتيجة
    result = Text(value="")

    # دالة لحساب سعر التيكت وتحديث المجموع في Text control
    def calc_price(e):
        total = 0
        extra_value = 0

        # حساب مجموع الشيك بوكسات في col1 و col2
        checkboxes = col1.controls + col2.controls
        for checkbox in checkboxes:
            if checkbox.value:
                item_price = items.get(checkbox.label, 0)
                total += item_price

        # حساب مجموع الشيك بوكسات في col3 فقط
        for checkbox in col3.controls:
            if checkbox.value:
                item_price2 = items2.get(checkbox.label, 0)
                extra_value += item_price2

        # تحديث قيمة النتيجة وتقسيمها على عدد الأفراد
        if num_of_person.value.isdigit() and int(num_of_person.value) > 0:
            result.value = (total / float(num_of_person.value)) + extra_value
        else:
            result.value = "يرجى إدخال عدد صحيح من الأفراد."
        page.update()

    # إعداد الأزرار وعناصر الواجهة
    edt_pric_btn  = ElevatedButton('إضافة أسعار', on_click=lambda _: page.go("/page2"), icon=icons.ADD, bgcolor="#102030", color="#ffffff")
    calc_pric_btn = ElevatedButton('سعر التذكرة', on_click=calc_price, icon=icons.CALCULATE_OUTLINED, bgcolor="#102030", color="#ffffff")

    # تعريف Checkboxes للبنود في الأعمدة
    col1 = Column([Checkbox(label="جليتر", value=False), Checkbox(label="برومو", value=False), Checkbox(label="درون", value=False),
                   Checkbox(label="دي جي", value=False), Checkbox(label="كلر", value=False), Checkbox(label="باندا", value=False),
                   Checkbox(label="درامز", value=False), Checkbox(label="استيدج", value=False), Checkbox(label="باصات *عدل ", value=False),
                   Checkbox(label="كمان", value=False), Checkbox(label="مسرح", value=False), Checkbox(label="كورال", value=False)],
                  spacing=5)

    col2 = Column([Checkbox(label="ناي", value=False), Checkbox(label="ساكس", value=False), Checkbox(label="تنظيم", value=False),
                   Checkbox(label="شماريخ", value=False), Checkbox(label="بالونات + اقلام", value=False), Checkbox(label="طبله", value=False),
                   Checkbox(label="جيتار", value=False), Checkbox(label="كاميرا 360", value=False), Checkbox(label="رحله نيلية", value=False),
                   Checkbox(label="العاب بامب", value=False), Checkbox(label="فقرات", value=False), Checkbox(label="ارت", value=False)],
                  spacing=5)

    col3 = Column([Checkbox(label="فوم", value=False), Checkbox(label="وجبة", value=False), Checkbox(label="عصير/كنز", value=False),
                   Checkbox(label="هودي /تيشرت", value=False), Checkbox(label="المكان", value=False), Checkbox(label="هدية", value=False),
                   Checkbox(label="درع + وشاح", value=False), Checkbox(label="مسدس", value=False),fom,fom,fom,fom],
                  spacing=5, alignment=MainAxisAlignment.CENTER)

    # تعريف واجهة الصفحة
    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                '/',
                [
                    AppBar(title=Text("Royal Team", size=20), color="white", bgcolor="#102030"),
                    Row([Text("بنود الحفل", size=20, color="#102030")], alignment=MainAxisAlignment.CENTER),
                    Row([col1, col2, col3], spacing=0, alignment=MainAxisAlignment.SPACE_AROUND, rtl=True),
                    Row([result, num_of_person], alignment=MainAxisAlignment.END),
                    Row([edt_pric_btn, calc_pric_btn], alignment=MainAxisAlignment.END),
                ]
            )
        )

        # صفحة تعديل الأسعار
        if page.route == "/page2":
            current_prices_items, current_prices_items2 = items, items2
            input_fields = {}

            # لحفظ الأسعار المحدثة
            def save_updated_prices(e):
                global items, items2
                for item, input_field in input_fields["items"].items():
                    if input_field.value.isdigit():
                        items[item] = int(input_field.value)
                for item, input_field in input_fields["items2"].items():
                    if input_field.value.isdigit():
                        items2[item] = int(input_field.value)

                save_prices_to_file(items, items2)

                # تحديث القيم المستخدمة
                items, items2 = load_prices_from_file()
                page.go("/")

            dialog_content = Container(
                content=ListView(spacing=10, padding=20, expand=True),
                expand=True
            )

            input_fields["items"] = {}
            input_fields["items2"] = {}

            for item, price in current_prices_items.items():
                input_field = TextField(
                    label=item,
                    value=str(price),
                    width=150,
                    text_align=TextAlign.RIGHT,
                    rtl=True
                )
                input_fields["items"][item] = input_field
                dialog_content.content.controls.append(input_field)

            for item, price in current_prices_items2.items():
                input_field = TextField(
                    label=item,
                    value=str(price),
                    width=150,
                    text_align=TextAlign.RIGHT,
                    rtl=True
                )
                input_fields["items2"][item] = input_field
                dialog_content.content.controls.append(input_field)

            page.views.append(
                View(
                    'page2',
                    [
                        AppBar(title=Text("تعديل الأسعار", size=20), color="white", bgcolor="#102030"),
                        dialog_content,
                        Row(
                            [
                                ElevatedButton('حفظ', on_click=save_updated_prices, icon=icons.SAVE, bgcolor="#102030", color="#ffffff"),
                            ],
                            alignment=MainAxisAlignment.CENTER
                        ),
                    ]
                )
            )

        page.update()

    def page_go(View):
        page.views.pop()
        back_page = page.views[-1]
        page.go(back_page.route)

    page.on_route_change = route_change
    page.on_view_pop = page_go
    page.go(page.route)

app(main)
