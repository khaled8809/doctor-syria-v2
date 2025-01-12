&lt;template&gt;
  &lt;div class="appointment-calendar"&gt;
    &lt;div class="calendar-header"&gt;
      &lt;button @click="previousMonth" class="nav-button"&gt;&lt;i class="fas fa-chevron-left"&gt;&lt;/i&gt;&lt;/button&gt;
      &lt;h2&gt;{{ currentMonthName }} {{ currentYear }}&lt;/h2&gt;
      &lt;button @click="nextMonth" class="nav-button"&gt;&lt;i class="fas fa-chevron-right"&gt;&lt;/i&gt;&lt;/button&gt;
    &lt;/div&gt;
    
    &lt;div class="calendar-grid"&gt;
      &lt;div v-for="day in weekDays" :key="day" class="day-header"&gt;{{ day }}&lt;/div&gt;
      &lt;div
        v-for="date in calendarDays"
        :key="date.date"
        :class="['calendar-day', { 
          'current-month': date.currentMonth,
          'has-appointments': hasAppointments(date.date),
          'selected': isSelected(date.date)
        }]"
        @click="selectDate(date.date)"
      &gt;
        &lt;span class="date-number"&gt;{{ date.dayOfMonth }}&lt;/span&gt;
        &lt;div class="appointment-indicators" v-if="hasAppointments(date.date)"&gt;
          &lt;span 
            v-for="(appointment, index) in getAppointments(date.date)"
            :key="index"
            class="indicator"
            :style="{ backgroundColor: getStatusColor(appointment.status) }"
            :title="appointment.patientName"
          &gt;&lt;/span&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
    
    &lt;div v-if="selectedDate" class="appointments-list"&gt;
      &lt;h3&gt;المواعيد في {{ formatDate(selectedDate) }}&lt;/h3&gt;
      &lt;div v-if="selectedDateAppointments.length === 0" class="no-appointments"&gt;
        لا توجد مواعيد في هذا اليوم
      &lt;/div&gt;
      &lt;div 
        v-for="appointment in selectedDateAppointments" 
        :key="appointment.id"
        class="appointment-item"
      &gt;
        &lt;div class="appointment-time"&gt;{{ formatTime(appointment.time) }}&lt;/div&gt;
        &lt;div class="appointment-details"&gt;
          &lt;div class="patient-name"&gt;{{ appointment.patientName }}&lt;/div&gt;
          &lt;div class="appointment-type"&gt;{{ appointment.type }}&lt;/div&gt;
          &lt;div class="appointment-status" :class="appointment.status"&gt;
            {{ getStatusText(appointment.status) }}
          &lt;/div&gt;
        &lt;/div&gt;
        &lt;div class="appointment-actions"&gt;
          &lt;button @click="editAppointment(appointment)" class="edit-btn"&gt;
            &lt;i class="fas fa-edit"&gt;&lt;/i&gt;
          &lt;/button&gt;
          &lt;button @click="cancelAppointment(appointment)" class="cancel-btn"&gt;
            &lt;i class="fas fa-times"&gt;&lt;/i&gt;
          &lt;/button&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script&gt;
import { ref, computed } from 'vue'
import { format, addMonths, subMonths, startOfMonth, endOfMonth, eachDayOfInterval } from 'date-fns'
import { ar } from 'date-fns/locale'

export default {
  name: 'AppointmentCalendar',
  props: {
    appointments: {
      type: Array,
      required: true
    }
  },
  
  setup(props) {
    const currentDate = ref(new Date())
    const selectedDate = ref(null)
    
    const weekDays = ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
    
    const currentMonthName = computed(() => {
      return format(currentDate.value, 'MMMM', { locale: ar })
    })
    
    const currentYear = computed(() => {
      return format(currentDate.value, 'yyyy')
    })
    
    const calendarDays = computed(() => {
      const start = startOfMonth(currentDate.value)
      const end = endOfMonth(currentDate.value)
      return eachDayOfInterval({ start, end }).map(date => ({
        date,
        dayOfMonth: format(date, 'd'),
        currentMonth: true
      }))
    })
    
    const selectedDateAppointments = computed(() => {
      if (!selectedDate.value) return []
      return props.appointments.filter(appointment => 
        format(new Date(appointment.date), 'yyyy-MM-dd') === 
        format(selectedDate.value, 'yyyy-MM-dd')
      )
    })
    
    const nextMonth = () => {
      currentDate.value = addMonths(currentDate.value, 1)
    }
    
    const previousMonth = () => {
      currentDate.value = subMonths(currentDate.value, 1)
    }
    
    const selectDate = (date) => {
      selectedDate.value = date
    }
    
    const hasAppointments = (date) => {
      return props.appointments.some(appointment => 
        format(new Date(appointment.date), 'yyyy-MM-dd') === 
        format(date, 'yyyy-MM-dd')
      )
    }
    
    const getAppointments = (date) => {
      return props.appointments.filter(appointment => 
        format(new Date(appointment.date), 'yyyy-MM-dd') === 
        format(date, 'yyyy-MM-dd')
      )
    }
    
    const getStatusColor = (status) => {
      const colors = {
        scheduled: '#4CAF50',
        completed: '#2196F3',
        cancelled: '#F44336',
        pending: '#FFC107'
      }
      return colors[status] || '#757575'
    }
    
    const getStatusText = (status) => {
      const texts = {
        scheduled: 'مجدول',
        completed: 'مكتمل',
        cancelled: 'ملغي',
        pending: 'قيد الانتظار'
      }
      return texts[status] || status
    }
    
    const formatDate = (date) => {
      return format(date, 'dd/MM/yyyy')
    }
    
    const formatTime = (time) => {
      return format(new Date(`2000-01-01T${time}`), 'HH:mm')
    }
    
    return {
      currentDate,
      selectedDate,
      weekDays,
      currentMonthName,
      currentYear,
      calendarDays,
      selectedDateAppointments,
      nextMonth,
      previousMonth,
      selectDate,
      hasAppointments,
      getAppointments,
      getStatusColor,
      getStatusText,
      formatDate,
      formatTime
    }
  }
}
&lt;/script&gt;

&lt;style scoped&gt;
.appointment-calendar {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.nav-button {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  color: #666;
  padding: 5px 10px;
  border-radius: 4px;
}

.nav-button:hover {
  background-color: #f5f5f5;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #eee;
  border: 1px solid #eee;
  border-radius: 4px;
}

.day-header {
  background: #f8f9fa;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  color: #495057;
}

.calendar-day {
  background: white;
  min-height: 100px;
  padding: 10px;
  position: relative;
  cursor: pointer;
}

.calendar-day:hover {
  background-color: #f8f9fa;
}

.date-number {
  position: absolute;
  top: 5px;
  right: 5px;
  color: #666;
}

.appointment-indicators {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  margin-top: 25px;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.appointments-list {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.appointment-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 10px;
}

.appointment-time {
  font-weight: bold;
  min-width: 80px;
}

.appointment-details {
  flex-grow: 1;
  margin: 0 20px;
}

.patient-name {
  font-weight: bold;
}

.appointment-type {
  color: #666;
  font-size: 0.9em;
}

.appointment-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  margin-top: 5px;
}

.appointment-status.scheduled { background-color: #e8f5e9; color: #4CAF50; }
.appointment-status.completed { background-color: #e3f2fd; color: #2196F3; }
.appointment-status.cancelled { background-color: #ffebee; color: #F44336; }
.appointment-status.pending { background-color: #fff3e0; color: #FFC107; }

.appointment-actions {
  display: flex;
  gap: 5px;
}

.appointment-actions button {
  background: none;
  border: none;
  padding: 5px;
  cursor: pointer;
  border-radius: 4px;
}

.edit-btn:hover { color: #2196F3; }
.cancel-btn:hover { color: #F44336; }

.no-appointments {
  text-align: center;
  color: #666;
  padding: 20px;
}

@media (max-width: 768px) {
  .calendar-day {
    min-height: 60px;
  }
  
  .appointment-indicators {
    margin-top: 20px;
  }
  
  .appointment-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .appointment-details {
    margin: 10px 0;
  }
}
&lt;/style&gt;
