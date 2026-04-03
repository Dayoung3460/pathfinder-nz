"""INZ document URLs for ingestion into ChromaDB.

All URLs are sourced from official Immigration New Zealand pages.
Update this file when INZ restructures or moves pages.
"""

EMPLOYER_URLS = [
    "https://www.immigration.govt.nz/employ-migrants/new-employer-accreditation-and-work-visa",
    "https://www.immigration.govt.nz/employ-migrants/new-employer-accreditation-and-work-visa/accreditation-types-and-employers-requirements",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/aewv-employer-accreditation-and-job-check-process/",
    "https://www.immigration.govt.nz/work/for-employers/hiring-people-from-overseas/making-a-job-offer/",
    "https://www.immigration.govt.nz/about-us/news-centre/accredited-employer-work-visa-aewv-key-information-and-statistics/",
    "https://www.immigration.govt.nz/about-us/news-centre/how-changes-to-the-accredited-employer-work-visa-aewv-may-affect-you/",
]

AEWV_URLS = [
    "https://www.immigration.govt.nz/visas/accredited-employer-work-visa/",
    "https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-work-visa",
    "https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions",
    "https://www.immigration.govt.nz/work/requirements-for-work-visas/approved-employers/accredited-employer-list/",
]

SMC_URLS = [
    "https://www.immigration.govt.nz/visas/skilled-migrant-category-resident-visa/",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/skilled-migrant-category-pathway-to-residence/",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/skilled-migrant-category-pathway-to-residence/pay-rates-for-the-skilled-migrant-category-resident-visa/",
    "https://www.immigration.govt.nz/formshelp/smc-eoi-form",
    "https://www.immigration.govt.nz/formshelp/smc-visa-application",
    "https://www.immigration.govt.nz/about-us/news-centre/further-changes-to-the-skilled-migrant-category-to-come-into-effect-in-august-2026/",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/",
    "https://www.immigration.govt.nz/process-to-apply/waiting-for-a-visa/interim-visas-so-you-can-stay-here-lawfully/skilled-migrant-category-interim-visa/",
]

PARTNER_URLS = [
    "https://www.immigration.govt.nz/process-to-apply/once-you-have-a-visa/bringing-family-to-new-zealand/partnership-and-how-to-prove-it/",
    "https://www.immigration.govt.nz/about-us/news-centre/partnership-visas/",
    "https://www.immigration.govt.nz/visas/partner-of-a-new-zealander-visa/",
    "https://www.immigration.govt.nz/visas/partner-of-a-student-work-visa/",
    "https://www.immigration.govt.nz/visas/partner-of-a-student-visitor-visa/",
]

STUDENT_URLS = [
    "https://www.immigration.govt.nz/study/study-visas/",
    "https://www.immigration.govt.nz/assist-migrants-and-students/assist-students/student-visa-info",
    "https://www.immigration.govt.nz/study/once-you-have-a-student-visa/check-or-change-your-student-visa-conditions/",
    "https://www.immigration.govt.nz/about-us/news-centre/upcoming-changes-to-student-visa-work-rights/",
    "https://www.immigration.govt.nz/process-to-apply/once-you-have-a-visa/bringing-family-to-new-zealand/bringing-family-on-a-student-visa/",
]

VOC_URLS = [
    "https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-work-visa",
    "https://www.immigration.govt.nz/study/once-you-have-a-student-visa/check-or-change-your-student-visa-conditions/",
    "https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-visitor-visa",
    "https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions",
    "https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions-student",
]

GENERAL_URLS = [
    "https://www.immigration.govt.nz/new-zealand-visas/preparing-a-visa-application/character-and-identity/good-character/supporting-partner-character",
    "https://www.immigration.govt.nz/process-to-apply/waiting-for-a-visa/interim-visas-so-you-can-stay-here-lawfully/interim-visa-conditions/",
]

ALL_URLS = (
    EMPLOYER_URLS
    + AEWV_URLS
    + SMC_URLS
    + PARTNER_URLS
    + STUDENT_URLS
    + VOC_URLS
    + GENERAL_URLS
)
