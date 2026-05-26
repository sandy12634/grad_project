#!/bin/bash

# ألوان للطباعة
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000/api"

echo -e "${YELLOW}=== اختبار Permissions ===${NC}\n"

# 1. تسجيل الدخول - Superadmin
echo -e "${YELLOW}1️⃣  تسجيل الدخول كـ Superadmin...${NC}"
SUPERADMIN_TOKEN=$(curl -s -X POST "$API_URL/accounts/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"superadmin_user","password":"password123"}' \
  | grep -o '"access":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}Token: $SUPERADMIN_TOKEN${NC}\n"

# 2. تسجيل الدخول - Admin (رياضة)
echo -e "${YELLOW}2️⃣  تسجيل الدخول كـ Admin (رياضة)...${NC}"
ADMIN_SPORTS_TOKEN=$(curl -s -X POST "$API_URL/accounts/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin_sports","password":"password123"}' \
  | grep -o '"access":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}Token: $ADMIN_SPORTS_TOKEN${NC}\n"

# 3. Admin تعليم يحاول الوصول
echo -e "${YELLOW}3️⃣  تسجيل الدخول كـ Admin (تعليم)...${NC}"
ADMIN_EDUCATION_TOKEN=$(curl -s -X POST "$API_URL/accounts/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin_education","password":"password123"}' \
  | grep -o '"access":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}Token: $ADMIN_EDUCATION_TOKEN${NC}\n"

# ==========================================
echo -e "${YELLOW}=== اختبار الوصول للبيانات ===${NC}\n"

# Test 1: Superadmin يرى كل البيانات
echo -e "${YELLOW}✅ Test 1: Superadmin يرى كل الأقطاع${NC}"
curl -s -X GET "$API_URL/content/events/" \
  -H "Authorization: Bearer $SUPERADMIN_TOKEN" | python -m json.tool
echo -e "\n"

# Test 2: Admin الرياضة يرى فقط بيانات الرياضة
echo -e "${YELLOW}✅ Test 2: Admin (رياضة) يرى فقط الرياضة${NC}"
curl -s -X GET "$API_URL/content/events/" \
  -H "Authorization: Bearer $ADMIN_SPORTS_TOKEN" | python -m json.tool
echo -e "\n"

# Test 3: Admin التعليم يحاول الوصول لبيانات الرياضة (يجب أن يرى 403 أو البيانات فارغة)
echo -e "${YELLOW}✅ Test 3: Admin (تعليم) يحاول حذف حدث رياضي${NC}"
curl -s -X DELETE "$API_URL/content/events/1/" \
  -H "Authorization: Bearer $ADMIN_EDUCATION_TOKEN" \
  -H "Content-Type: application/json"
echo -e "\n"

echo -e "${GREEN}=== انتهى الاختبار ===${NC}"
