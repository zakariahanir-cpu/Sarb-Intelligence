# Sarb Intelligence

مشروع Python لوكيل ذكي واحد باسم `agent_epsilon` مع أدوات للتعلم وحفظ الذاكرة
والبحث وبناء مشاريع ويب.

## التشغيل السريع

شغّل فحصًا محليًا لا يحتاج إلى مفتاح API:

```bash
python3 main.py --check
```

لتشغيل مهمة فعلية، أضف السر `EPSILON_GROQ` ثم شغّل:

```bash
python3 main.py "حلّل سجل الرسائل"
```

## الاختبارات

```bash
python3 -m unittest discover -s tests -v
```

## GitHub Actions

يشغّل الملف `.github/workflows/agents_swarm.yml` فحص الصحة كل ساعة أو عند
التشغيل اليدوي. تم تصحيح المسارات ليستخدم بنية المستودع الحالية بدل مسارات
قديمة مثل `shared_tools/` و`agents/agent_alpha/` التي لم تكن موجودة.

يمكن تشغيل الوكيل الفعلي على GitHub بعد إضافة `EPSILON_GROQ` إلى Secrets، أما
فحص الصحة فلا يحتاج إلى أي سر.
