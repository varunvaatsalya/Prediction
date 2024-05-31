import pandas as pd
from django.shortcuts import render
from .forms import CSVUploadForm

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            df = pd.read_excel(csv_file)
            print("Columns in the DataFrame:", df.columns)
            if 'Cust State' not in df.columns or 'DPD' not in df.columns:
                return render(request, 'error.html', {'message': 'Required columns not found in the uploaded file'})


            summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
            summary = summary.rename(columns={'Cust State': 'State'})


            summary['Row_Number'] = summary.index + 1

            context = {
                'form': form,
                'summary': summary.to_dict(orient='records')
            }
            return render(request, 'upload.html', context)
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})
