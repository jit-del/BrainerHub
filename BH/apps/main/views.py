import csv
import openpyxl
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Employee
from .serializers import EmployeeSerializer,CompanySerializer

class InsertDataFromExcel(APIView):
    def post(self, request, format=None):
        file = request.FILES['file']  # Assuming the file is uploaded via a POST request field called 'file'

        try:
            if file.name.endswith('.csv'):
                # Read the uploaded file as CSV
                decoded_file = file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                data = list(reader)
            elif file.name.endswith('.xlsx'):
                # Read the uploaded file as Excel
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                data = []
                headers = [cell.value for cell in sheet[1]]
                for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
                    data.append(dict(zip(headers, row)))
            if not data:
                return Response({'error': 'Invalid file format'}, status=status.HTTP_400_BAD_REQUEST)

            # Create unique companies from the data
            companies_data = set(row['COMPANY_NAME'] for row in data)
            companies_data_list=[]

            for company_name in companies_data:
                companies_data_list.append({'company_name': company_name})
                
            company_serializer = CompanySerializer(data=companies_data_list,many=True)
            if company_serializer.is_valid():
                company_serializer.save()

            # Prepare employee data with corresponding company foreign keys
            employees_data = []
            for row in data:
                if (
                    row.get('SALARY') and
                    row.get('MANAGER_ID') and
                    row.get('DEPARTMENT_ID')
                ):
                    company = Company.objects.get(company_name=row['COMPANY_NAME'])
                    employees_data.append({
                        'first_name': row['FIRST_NAME'],
                        'last_name': row['LAST_NAME'],
                        'phone_number': row['PHONE_NUMBER'],
                        'company': company.id,
                        'salary': int(row['SALARY']),
                        'manager_id': int(row['MANAGER_ID']),
                        'department_id': int(row['DEPARTMENT_ID'])
                    })

            # Use the serializer to insert employees in bulk
            employee_serializer = EmployeeSerializer(data=employees_data, many=True)
            if employee_serializer.is_valid():
                employee_serializer.save()
                return Response({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': employee_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
