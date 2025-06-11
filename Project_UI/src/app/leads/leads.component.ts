import { Component, ElementRef, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { TabsComponent } from '../tabs/tabs.component';
import { AgGridModule } from 'ag-grid-angular';
import { ColDef, GridOptions } from 'ag-grid-community';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { N8nService } from '../services/n8n/n8n.service';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MessageService } from '../services/messageService/message.service';
import { LeadsServiceTs } from '../services/leadsService/leads.service.ts';
import { LoaderComponent } from '../loader/loader.component';
import { ChatComponent } from '../chat/chat.component';

interface ChatMessage {
  text: string;
  isUser: boolean;
  timestamp: Date;
}

interface Lead {
  lead_first_name: string;
  lead_last_name: string;
  lead_company_name: string;
  lead_official_title: string;
  lead_type: string;
  lead_generation_source: string;
  lead_status: string;
  lead_contact_number: string;
  selected?: boolean;
}

@Component({
  selector: 'app-leads',
  imports: [TabsComponent, CommonModule, FormsModule, AgGridModule, MatSnackBarModule, LoaderComponent, ChatComponent],
  templateUrl: './leads.component.html',
  styleUrls: ['./leads.component.scss'],
  standalone: true,
})

export class LeadsComponent implements OnInit {

  constructor(private router: Router, private n8nService: N8nService, private snackBar: MatSnackBar, private leadsServiceTs: LeadsServiceTs, private messageService: MessageService) { }
  
    rowData: Lead[] = [];
    loading: boolean = false;

  private loadLeadsData(): void {
  this.loading = true;
  this.rowData = []; // Clear current data

  this.leadsServiceTs.getLeadsData().subscribe({
    next: (data) => {
      (Array.isArray(data) ? data : []).forEach((ele: any) => {
        let lead: Lead = {
          lead_first_name: ele.lead_first_name || '--',
          lead_last_name: ele.lead_last_name || '--',
          lead_company_name: ele.lead_company_name || '--',
          lead_official_title: ele.lead_official_title || '--',
          lead_type: ele.lead_type || '--',
          lead_generation_source: ele.lead_generation_source || '--',
          lead_status: ele.lead_status || '--',
          lead_contact_number: ele.lead_contact_number || '--',
        };
        this.rowData.push(lead);
      });
      this.rowData = [...this.rowData];
      this.loading = false;
    },
    error: (error) => {
      console.error('Error fetching leads data:', error);
      this.snackBar.open('Failed to load leads data', '', { duration: 3000 });
      this.loading = false;
    }
  });
}


  ngOnInit(): void {
  this.loadLeadsData();
}


  @Output() tabChanged = new EventEmitter<{ tab: string; clientId: string | null }>();

  @ViewChild('chatMessages') private chatMessagesContainer!: ElementRef;

  clientId: string = '';
  messages: ChatMessage[] = [
    {
      text: 'Hello! How can I help you today?',
      isUser: false,
      timestamp: new Date(),
    },
  ];

  currentMessage: string = '';
  private shouldScrollToBottom = false;
  isChatOpen: boolean = false;
  selectedLeads: Lead[] = [];

  // AG Grid properties
  columnDefs: ColDef[] = [
    {
      headerName: '',
      checkboxSelection: true,
      headerCheckboxSelection: true,
      width: 60,
      minWidth: 60,
      maxWidth: 60,
      pinned: 'left',
      resizable: false,
      sortable: false,
      filter: false,
      cellStyle: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '8px'
      }
    },
    {
      headerName: 'First Name',
      field: 'lead_first_name',
      sortable: true,
      filter: true,
      flex: 1,
      minWidth: 120,
      cellStyle: { display: 'flex', alignItems: 'center', fontWeight: '500' }
    },
    {
      headerName: 'Last Name',
      field: 'lead_last_name',
      sortable: true,
      filter: true,
      flex: 1,
      minWidth: 120,
      cellStyle: { display: 'flex', alignItems: 'center', fontWeight: '500' }
    },
    {
      headerName: 'Company',
      field: 'lead_company_name',
      sortable: true,
      filter: true,
      flex: 1,
      minWidth: 160,
      cellStyle: { display: 'flex', alignItems: 'center', color: '#008080', fontWeight: '500' }
    },
    {
      headerName: 'Title',
      field: 'lead_official_title',
      sortable: true,
      filter: true,
      flex: 1,
      minWidth: 160,
      cellStyle: { display: 'flex', alignItems: 'center', fontStyle: 'italic', color: '#555' }
    },
    {
      headerName: 'Type',
      field: 'lead_type',
      sortable: true,
      filter: true,
      width: 100,
      cellRenderer: (params: any) => {
        const type = params.value;
        const colors: any = {
          'prospect': '#17a2b8',
          'qualified': '#28a745',
          'hot': '#dc3545'
        };
        return `<span style="
          background: ${colors[type] || '#6c757d'};
          color: white;
          padding: 4px 8px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 600;
          text-transform: uppercase;
        ">${type}</span>`;
      },
      cellStyle: { display: 'flex', alignItems: 'center' }
    },
    {
      headerName: 'Source',
      field: 'lead_generation_source',
      sortable: true,
      filter: true,
      flex: 1,
      minWidth: 120,
      cellStyle: { display: 'flex', alignItems: 'center', color: '#6c757d' }
    },
    {
      headerName: 'Status',
      field: 'lead_status',
      sortable: true,
      filter: true,
      width: 130,
      cellRenderer: (params: any) => {
        const status = params.value;
        const colors: any = {
          'new': '#007bff',
          'contacted': '#ffc107',
          'meeting_scheduled': '#28a745',
          'closed': '#6c757d'
        };
        return `<span style="
          background: ${colors[status] || '#6c757d'};
          color: white;
          padding: 4px 8px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 600;
          text-transform: uppercase;
        ">${status.replace('_', ' ')}</span>`;
      },
      cellStyle: { display: 'flex', alignItems: 'center' }
    },
    {
      headerName: 'Contact',
      field: 'lead_contact_number',
      sortable: true,
      filter: true,
      flex: 1,
      minWidth: 120,
      cellStyle: { display: 'flex', alignItems: 'center', fontFamily: 'monospace', color: '#008080' }
    }
  ];



  // Default column definitions
  defaultColDef: ColDef = {
    resizable: true,
    sortable: true,
    filter: true,
    minWidth: 100,
  };

  // AG Grid ready handler
  onGridReady(params: any) {
    params.api.sizeColumnsToFit();
  }

  // AG Grid selection change handler
  onSelectionChanged(event: any): void {
    this.selectedLeads = event.api.getSelectedRows();
    console.log('Selected leads:', this.selectedLeads);
  }

  // Trigger KYC function
  triggerKYC(): void {
    if (this.selectedLeads.length > 0) {
      const selectedNames = this.selectedLeads.map(lead =>
        `${lead.lead_first_name} ${lead.lead_last_name}`
      ).join(', ');

      const selectedNumber = this.selectedLeads.map(lead => lead.lead_contact_number).join(', ');
      
      
      // Add KYC logic here
      this.n8nService.getN8nData(selectedNumber).subscribe({
        next: (response: any) => {
          console.log('Response from n8n:', response);
          this.snackBar.open(response, '', { duration: 5000 });
          this.loadLeadsData();
        },
        error: (error) => {
          console.error('Error fetching data from n8n:', error);
          this.shouldScrollToBottom = true;
        },
      });
      console.log('Triggering KYC for selected leads:', this.selectedLeads);

      // // Add a chat message about the KYC trigger
      // this.messages.push({
      //   text: `KYC process initiated for ${this.selectedLeads.length} lead(s): ${selectedNames}`,
      //   isUser: false,
      //   timestamp: new Date(),
      // });
      this.shouldScrollToBottom = true;
    }
  }

  // Check if any leads are selected
  get hasSelectedLeads(): boolean {
    return this.selectedLeads.length > 0;
  }

  sendMessage(): void {
    const message = this.currentMessage.trim();

    if (message) {
      this.messages.push({
        text: message,
        isUser: true,
        timestamp: new Date(),
      });

      this.currentMessage = '';
      this.shouldScrollToBottom = true;

      this.messageService.sendMessageToApi(message).subscribe({
        next: (response: string) => {
          this.messages.push({
            text: response,
            isUser: false,
            timestamp: new Date(),
          });
          this.shouldScrollToBottom = true;
        },
        error: (error) => {
          this.messages.push({
            text: `An error occurred: ${error.message}`,
            isUser: false,
            timestamp: new Date(),
          });
          this.shouldScrollToBottom = true;
        }
      });
    }
  }


  handleKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.sendMessage();
    }
  }

  // Toggle chat visibility
  toggleChat(): void {
    this.isChatOpen = !this.isChatOpen;
    if (this.isChatOpen) {
      // Scroll to bottom when chat opens
      setTimeout(() => {
        this.shouldScrollToBottom = true;
      }, 100);
    }
  }

  ngAfterViewChecked(): void {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  private scrollToBottom(): void {
    try {
      if (this.chatMessagesContainer) {
        this.chatMessagesContainer.nativeElement.scrollTop =
          this.chatMessagesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.error('Error scrolling to bottom:', err);
    }
  }
}