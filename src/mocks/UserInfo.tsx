export const usersData = [
  {
    status: 'confirmed',
    name: 'Зубенко Михаил Петрович',
    inn: '0123456789',
    address: 'Северная ул., 405, Краснодар',
    avgConsumption: '480 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 36,
    fillRate: 0.83,
    tariff: 4.28,
    damagePerMonth: 4396,
    damagePerYear: 52800,
    damageMultiplier: 3,

    businessInfo: 'ИП Иванов С.П. зарегистрирован “Ремонт бытовой техники”',
    miningProbability: 'высокая',
    nightLoad: 'Повышенная ночная нагрузка;',
    seasonalityAbsence: 'Отсутствие сезонности.',

    recommendations: [
      'Провести проверку адреса на фактическое ведение деятельности',
      'Предложить переход на другой тариф',
      'При отказе — инициировать перерасчёт за 3 месяца с доначислением по тарифу «прочие потребители»',
      'В случае подтверждения — оформить акт нецелевого использования',
    ],

    history: [
      '05.03 — отправлено уведомление, начато расследование',
      '10.03 — предложено изменить тариф, зафиксированы отклонения',
      '20.03 — проведён повторный контроль, рекомендован переход на иной тариф',
    ],
  },
  {
    status: 'confirmed',
    name: 'Петров Иван Сергеевич',
    inn: '9876543210',
    address: 'ул. Ленина, 10, Краснодар',
    avgConsumption: '320 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 24,
    fillRate: 0.75,
    tariff: 3.98,
    damagePerMonth: 3100,
    damagePerYear: 37200,
    damageMultiplier: 2,

    businessInfo: 'ИП Петров И.С. зарегистрирован “Торговля бытовой техникой”',
    miningProbability: 'средняя',
    nightLoad: 'Повышенная дневная нагрузка;',
    seasonalityAbsence: 'Сезонность выражена.',

    recommendations: [
      'Проверить актуальность регистрации',
      'Рассмотреть возможность корректировки тарифа',
      'Мониторить изменения потребления ежемесячно',
      'В случае выявления отклонений — провести аудит',
    ],

    history: [
      '01.02 — проверка регистрации',
      '15.02 — рекомендации по тарифу отправлены',
      '01.03 — мониторинг изменений потребления начат',
    ],
  },
  {
    status: 'notConfirmed',
    name: 'Иванова Анна Викторовна',
    inn: '1234598765',
    address: 'пр. Красный, 5, Краснодар',
    avgConsumption: '150 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 15,
    fillRate: 0.9,
    tariff: 4.50,
    damagePerMonth: 2100,
    damagePerYear: 25200,
    damageMultiplier: 1.5,

    businessInfo: 'Нет зарегистрированного бизнеса',
    miningProbability: 'низкая',
    nightLoad: 'Повышенная нагрузка отсутствует;',
    seasonalityAbsence: 'Сезонность не выражена.',

    recommendations: [
      'Провести разъяснительную работу',
      'Обратить внимание на сезонные колебания',
      'Рассмотреть возможности оптимизации потребления',
      'Регулярно отслеживать отклонения',
    ],

    history: [
      '10.01 — направлено предупреждение',
      '20.01 — проведён мониторинг',
      '05.02 — рекомендованы меры по оптимизации',
    ],
  },
  {
    status: 'confirmed',
    name: 'Сидоров Алексей Николаевич',
    inn: '1122334455',
    address: 'ул. Пушкина, 25, Краснодар',
    avgConsumption: '400 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 30,
    fillRate: 0.85,
    tariff: 4.10,
    damagePerMonth: 3800,
    damagePerYear: 45600,
    damageMultiplier: 2.8,

    businessInfo: 'ИП Сидоров А.Н. зарегистрирован “Ремонт техники”',
    miningProbability: 'высокая',
    nightLoad: 'Повышенная ночная нагрузка;',
    seasonalityAbsence: 'Отсутствие сезонности.',

    recommendations: [
      'Провести дополнительный аудит',
      'Рассмотреть корректировку тарифа',
      'Усилить контроль за ночной нагрузкой',
      'Обеспечить соответствие сезонным требованиям',
    ],

    history: [
      '15.03 — инициирована проверка',
      '22.03 — рекомендации переданы клиенту',
      '30.03 — контроль за ночной нагрузкой усилен',
    ],
  },
  {
    status: 'confirmed',
    name: 'Кузнецова Мария Владимировна',
    inn: '5566778899',
    address: 'ул. Красная, 77, Краснодар',
    avgConsumption: '350 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 28,
    fillRate: 0.78,
    tariff: 4.00,
    damagePerMonth: 3200,
    damagePerYear: 38400,
    damageMultiplier: 1.9,

    businessInfo: 'ИП Кузнецова М.В. зарегистрирован “Ремонт электроники”',
    miningProbability: 'средняя',
    nightLoad: 'Повышенная нагрузка вечером;',
    seasonalityAbsence: 'Сезонность частичная.',

    recommendations: [
      'Проверить соответствие документооборота',
      'Рассмотреть возможность изменения тарифа',
      'Мониторить потребление в ночные часы',
      'Провести аудит сезонных колебаний',
    ],

    history: [
      '05.04 — проверка документов',
      '15.04 — предложение по тарифу',
      '22.04 — аудит сезонных колебаний',
    ],
  },
  {
    status: 'notConfirmed',
    name: 'Васильев Сергей Анатольевич',
    inn: '6677889900',
    address: 'ул. Советская, 99, Краснодар',
    avgConsumption: '200 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 18,
    fillRate: 0.7,
    tariff: 3.85,
    damagePerMonth: 2200,
    damagePerYear: 26400,
    damageMultiplier: 1.4,

    businessInfo: 'Нет зарегистрированного бизнеса',
    miningProbability: 'низкая',
    nightLoad: 'Ночная нагрузка отсутствует;',
    seasonalityAbsence: 'Сезонность выражена.',

    recommendations: [
      'Обратиться в налоговую',
      'Пересмотреть тарифные планы',
      'Следить за сезонными изменениями',
      'Регулярно проверять показатели потребления',
    ],

    history: [
      '12.05 — отправлено уведомление',
      '22.05 — пересмотр тарифов',
      '30.05 — анализ потребления',
    ],
  },
  {
    status: 'confirmed',
    name: 'Николаев Андрей Павлович',
    inn: '7788990011',
    address: 'ул. Гагарина, 12, Краснодар',
    avgConsumption: '280 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 27,
    fillRate: 0.8,
    tariff: 4.22,
    damagePerMonth: 3500,
    damagePerYear: 42000,
    damageMultiplier: 2.3,

    businessInfo: 'ИП Николаев А.П. зарегистрирован “Техническое обслуживание”',
    miningProbability: 'высокая',
    nightLoad: 'Повышенная ночная нагрузка;',
    seasonalityAbsence: 'Отсутствие сезонности.',

    recommendations: [
      'Проверить техническое состояние оборудования',
      'Рассмотреть корректировку тарифов',
      'Усилить контроль за аномалиями',
      'Обеспечить регулярное обучение персонала',
    ],

    history: [
      '08.06 — проверка оборудования',
      '18.06 — рекомендации направлены',
      '25.06 — обучение персонала',
    ],
  },
  {
    status: 'confirmed',
    name: 'Смирнова Елена Викторовна',
    inn: '8899001122',
    address: 'ул. Чехова, 45, Краснодар',
    avgConsumption: '360 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 29,
    fillRate: 0.82,
    tariff: 4.05,
    damagePerMonth: 3300,
    damagePerYear: 39600,
    damageMultiplier: 2.1,

    businessInfo: 'ИП Смирнова Е.В. зарегистрирован “Ремонт бытовой техники”',
    miningProbability: 'средняя',
    nightLoad: 'Повышенная дневная нагрузка;',
    seasonalityAbsence: 'Сезонность выражена.',

    recommendations: [
      'Проверить наличие документов',
      'Рассмотреть изменение тарифных условий',
      'Мониторить показатели потребления',
      'Проводить регулярные аудиты',
    ],

    history: [
      '02.07 — проверка документов',
      '12.07 — аудит тарифов',
      '22.07 — мониторинг потребления',
    ],
  },
  {
    status: 'notConfirmed',
    name: 'Федоров Михаил Юрьевич',
    inn: '9900112233',
    address: 'ул. Мира, 17, Краснодар',
    avgConsumption: '170 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 16,
    fillRate: 0.88,
    tariff: 4.40,
    damagePerMonth: 2400,
    damagePerYear: 28800,
    damageMultiplier: 1.7,

    businessInfo: 'Нет зарегистрированного бизнеса',
    miningProbability: 'низкая',
    nightLoad: 'Ночная нагрузка отсутствует;',
    seasonalityAbsence: 'Сезонность не выражена.',

    recommendations: [
      'Провести повторную проверку',
      'Анализировать ночную нагрузку',
      'Оценить сезонные факторы',
      'Проводить регулярные проверки',
    ],

    history: [
      '15.08 — проверка завершена',
      '25.08 — ночной анализ проведён',
      '05.09 — проверка сезонности',
    ],
  },

  {
    status: 'confirmed',
    name: 'Козлова Ирина Сергеевна',
    inn: '1010101010',
    address: 'ул. Гагарина, 5, Краснодар',
    avgConsumption: '390 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 31,
    fillRate: 0.80,
    tariff: 4.15,
    damagePerMonth: 3650,
    damagePerYear: 43800,
    damageMultiplier: 2.5,

    businessInfo: 'ИП Козлова И.С. зарегистрирован “Автосервис”',
    miningProbability: 'средняя',
    nightLoad: 'Умеренная ночная нагрузка;',
    seasonalityAbsence: 'Частичная сезонность.',

    recommendations: [
      'Проверить правильность ведения учета',
      'Оптимизировать тарифные планы',
      'Анализировать ночные нагрузки ежемесячно',
      'Проводить аудит в сезон пиковых нагрузок',
    ],

    history: [
      '10.04 — проведена проверка',
      '18.04 — рекомендации по тарифу',
      '25.04 — начат аудит ночных нагрузок',
    ],
  },
  {
    status: 'notConfirmed',
    name: 'Воробьев Андрей Михайлович',
    inn: '2020202020',
    address: 'пр. Ленина, 32, Краснодар',
    avgConsumption: '210 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 17,
    fillRate: 0.92,
    tariff: 4.55,
    damagePerMonth: 2550,
    damagePerYear: 30600,
    damageMultiplier: 1.8,

    businessInfo: 'Нет зарегистрированного бизнеса',
    miningProbability: 'низкая',
    nightLoad: 'Ночная нагрузка отсутствует;',
    seasonalityAbsence: 'Отсутствие сезонности.',

    recommendations: [
      'Провести разъяснительную работу',
      'Следить за аномалиями потребления',
      'Оптимизировать расход электроэнергии',
      'Проверять сезонные колебания',
    ],

    history: [
      '12.05 — направлено предупреждение',
      '22.05 — проведён мониторинг',
      '30.05 — рекомендованы меры по оптимизации',
    ],
  },
  {
    status: 'confirmed',
    name: 'Смирнов Алексей Викторович',
    inn: '3030303030',
    address: 'ул. Чехова, 50, Краснодар',
    avgConsumption: '430 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 33,
    fillRate: 0.87,
    tariff: 4.35,
    damagePerMonth: 4000,
    damagePerYear: 48000,
    damageMultiplier: 2.9,

    businessInfo: 'ИП Смирнов А.В. зарегистрирован “Производство мебели”',
    miningProbability: 'высокая',
    nightLoad: 'Высокая ночная нагрузка;',
    seasonalityAbsence: 'Отсутствие сезонности.',

    recommendations: [
      'Усилить контроль потребления ночью',
      'Рассмотреть изменение тарифа',
      'Провести дополнительный аудит',
      'Обеспечить обучение персонала',
    ],

    history: [
      '05.06 — инициирована проверка',
      '15.06 — рекомендации направлены',
      '25.06 — усилен контроль ночной нагрузки',
    ],
  },
  {
    status: 'confirmed',
    name: 'Куликова Наталья Петровна',
    inn: '4040404040',
    address: 'ул. Победы, 14, Краснодар',
    avgConsumption: '270 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 22,
    fillRate: 0.76,
    tariff: 4.05,
    damagePerMonth: 2800,
    damagePerYear: 33600,
    damageMultiplier: 2.0,

    businessInfo: 'ИП Куликова Н.П. зарегистрирован “Розничная торговля”',
    miningProbability: 'средняя',
    nightLoad: 'Средняя дневная нагрузка;',
    seasonalityAbsence: 'Частичная сезонность.',

    recommendations: [
      'Проверить соответствие документов',
      'Оптимизировать тарифные планы',
      'Мониторить сезонные колебания',
      'Регулярно проводить аудит',
    ],

    history: [
      '03.07 — проверка документов',
      '10.07 — оптимизация тарифов',
      '20.07 — аудит сезонных колебаний',
    ],
  },
  {
    status: 'notConfirmed',
    name: 'Морозов Сергей Николаевич',
    inn: '5050505050',
    address: 'ул. Лермонтова, 77, Краснодар',
    avgConsumption: '180 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 16,
    fillRate: 0.7,
    tariff: 3.9,
    damagePerMonth: 2000,
    damagePerYear: 24000,
    damageMultiplier: 1.5,

    businessInfo: 'Нет зарегистрированного бизнеса',
    miningProbability: 'низкая',
    nightLoad: 'Ночная нагрузка отсутствует;',
    seasonalityAbsence: 'Выраженная сезонность.',

    recommendations: [
      'Пересмотреть тарифные планы',
      'Обратить внимание на сезонность',
      'Оптимизировать потребление',
      'Проводить регулярный мониторинг',
    ],

    history: [
      '11.08 — предупреждение направлено',
      '21.08 — пересмотр тарифов',
      '31.08 — мониторинг потребления',
    ],
  },
  {
    status: 'confirmed',
    name: 'Новикова Светлана Викторовна',
    inn: '6060606060',
    address: 'ул. Советская, 18, Краснодар',
    avgConsumption: '350 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 29,
    fillRate: 0.82,
    tariff: 4.3,
    damagePerMonth: 3600,
    damagePerYear: 43200,
    damageMultiplier: 2.6,

    businessInfo: 'ИП Новикова С.В. зарегистрирован “Услуги связи”',
    miningProbability: 'высокая',
    nightLoad: 'Высокая ночная нагрузка;',
    seasonalityAbsence: 'Отсутствие сезонности.',

    recommendations: [
      'Провести аудит услуг связи',
      'Усилить контроль за ночным потреблением',
      'Рассмотреть корректировку тарифа',
      'Обеспечить обучение сотрудников',
    ],

    history: [
      '05.09 — начат аудит',
      '15.09 — контроль за потреблением усилен',
      '25.09 — обучение сотрудников проведено',
    ],
  },
  {
    status: 'confirmed',
    name: 'Егоров Дмитрий Александрович',
    inn: '7070707070',
    address: 'ул. Кирова, 3, Краснодар',
    avgConsumption: '310 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 26,
    fillRate: 0.79,
    tariff: 4.1,
    damagePerMonth: 3200,
    damagePerYear: 38400,
    damageMultiplier: 2.1,

    businessInfo: 'ИП Егоров Д.А. зарегистрирован “Ремонт автомобилей”',
    miningProbability: 'средняя',
    nightLoad: 'Средняя ночная нагрузка;',
    seasonalityAbsence: 'Частичная сезонность.',

    recommendations: [
      'Проверить техническое состояние',
      'Оптимизировать тарифы',
      'Мониторить ночное потребление',
      'Проводить регулярный аудит',
    ],

    history: [
      '12.10 — проверка состояния',
      '22.10 — оптимизация тарифов',
      '01.11 — аудит ночного потребления',
    ],
  },
  {
    status: 'notConfirmed',
    name: 'Григорьева Ольга Васильевна',
    inn: '8080808080',
    address: 'ул. Мира, 55, Краснодар',
    avgConsumption: '160 кВт/сут',
    riskLevel: 'high',

    averageConsumptionValue: 14,
    fillRate: 0.88,
    tariff: 4.45,
    damagePerMonth: 2300,
    damagePerYear: 27600,
    damageMultiplier: 1.7,

    businessInfo: 'Нет зарегистрированного бизнеса',
    miningProbability: 'низкая',
    nightLoad: 'Ночная нагрузка отсутствует;',
    seasonalityAbsence: 'Сезонность не выражена.',

    recommendations: [
      'Провести разъяснительную работу',
      'Следить за ночными изменениями',
      'Оценить сезонные факторы',
      'Регулярно проводить проверки',
    ],

    history: [
      '15.11 — направлено предупреждение',
      '25.11 — проведён мониторинг',
      '05.12 — рекомендованы меры',
    ],
  },
  {
    status: 'confirmed',
    name: 'Михайлова Наталья Ивановна',
    inn: '9090909090',
    address: 'пр. Ленина, 23, Краснодар',
    avgConsumption: '330 кВт/сут',
    riskLevel: 'medium',

    averageConsumptionValue: 27,
    fillRate: 0.81,
    tariff: 4.05,
    damagePerMonth: 3400,
    damagePerYear: 40800,
    damageMultiplier: 2.3,

    businessInfo: 'ИП Михайлова Н.И. зарегистрирован “Торговля запчастями”',
    miningProbability: 'средняя',
    nightLoad: 'Средняя дневная нагрузка;',
    seasonalityAbsence: 'Частичная сезонность.',

    recommendations: [
      'Проверить документооборот',
      'Рассмотреть изменение тарифов',
      'Мониторить дневное потребление',
      'Проводить регулярные аудиты',
    ],

    history: [
      '01.12 — проверка документов',
      '11.12 — аудит тарифов',
      '21.12 — мониторинг потребления',
    ],
  },
];
