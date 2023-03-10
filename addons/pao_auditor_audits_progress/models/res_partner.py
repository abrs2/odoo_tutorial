from odoo import fields, models, api
from datetime import *
from calendar import monthrange
import logging

_logger = logging.getLogger(__name__)

class RestPartnerInherit(models.Model):
    
    _inherit = "res.partner"

    audits_done = fields.Integer('Audits Done', readonly=True, compute="_compute_audits_number")
    progress_bar = fields.Integer('Progress', readonly=True, compute="_compute_audits_progress_bar")

    @api.depends("paa_audit_quantity")
    def _compute_audits_number(self):
       
        for rec in self:
            period =self._get_start_and_end_period_dates()
            start_date=datetime.strptime(period[0], '%Y-%m-%d').date()
            end_date=datetime.strptime(period[1], '%Y-%m-%d').date()
            if rec.ado_is_auditor:
                if not rec.paa_audit_quantity==0:
                    counter = 0
                    domain = [('partner_id', '=', rec.id),('service_start_date','>=',start_date),('service_start_date','<=',end_date),('state','!=','cancel'),('po_ac_audit_confirmation_status', 'in', ['1'])]
                    purchaseordeline = self.env['purchase.order.line'].search(domain)
                    
                    for r in purchaseordeline:
                        qty = r.product_qty
                        for p in r.product_id:
                            for c in p.categ_id:
                                if c.paa_is_an_audit:
                                    counter+=qty
                                                                
                    rec.audits_done=counter
                else: 
                    rec.audits_done=0
            else:
                rec.audits_done=0
            
        r=self._get_start_and_end_period_dates()
        
        _logger.error("--------------------------- R1 start date -> "+str(r[0])+" ------------ end date -> "+str(r[1])+"-------------------------------------")

            
    @api.depends("paa_audit_quantity")
    def _compute_audits_progress_bar(self):
        
        for u in self:
            period =self._get_start_and_end_period_dates()
            start_date=datetime.strptime(period[0], '%Y-%m-%d').date()
            end_date=datetime.strptime(period[1], '%Y-%m-%d').date()
            if u.ado_is_auditor:
                if u.paa_audit_quantity:
                    if not u.paa_audit_quantity==0:
                        audits_number = 0
                        #audits_number = (int) (u._get_audits_number/u.audits_target)*100     
                        domain = [('partner_id', '=', u.id),('service_start_date','>=',start_date),('service_start_date','<=',end_date),('state','!=','cancel'),('po_ac_audit_confirmation_status', 'in', ['1'])]
                        purchaseordeline = self.env['purchase.order.line'].search(domain)
                        for r in purchaseordeline:
                            qty = r.product_qty
                            for p in r.product_id:
                                for c in p.categ_id:
                                    if c.paa_is_an_audit:
                                        audits_number+=qty
                                        
                        #progress = (int) (audits_number/u.audits_target)*100
                        progress = audits_number/u.paa_audit_quantity
                        u.progress_bar= (int) (progress*100)
                    else:
                        u.progress_bar = 0
                else:
                    u.progress_bar = 0
            else:
                u.progress_bar = 0

    def _get_start_and_end_period_dates(self):
        
        start_date = ""
        end_date= ""
        configuration = self.env['paoassignmentauditor.configuration.audit.quantity'].search([])
        #today=datetime.strptime("2022-09-01", '%Y-%m-%d').date()
        today=datetime.today()
        anio= today.year
        mes= today.month
        dia= today.day
        diaInicial = ""
        mesInicial = ""
        anioInicial = ""
        diaFinal = ""
        mesFinal = ""
        anioFinal = ""

        for con in configuration:

            ms = int(con.season_start_month)
            me = int(con.season_end_month)

            if con.option == "auditor":

                if ms > mes:
                    anioInicial= anio-1
                    anioFinal= anio
                elif ms <= mes:
                    anioInicial= anio
                    anioFinal= anio+1

                mesInicial = ms
                mesFinal = me

            elif con.option == "month":
                
                for month in con.audits_quantity_per_month_ids:
                    ms = int(month.month)
                    if ms == mes:
                        anioInicial= anio
                        mesInicial = mes
                        anioFinal = anio
                        mesFinal = mes

            elif con.option == "trimester":
                
                anioInicioTemporada=""

                if ms > mes:
                    anioInicioTemporada= anio-1
                elif ms <= mes:
                    anioInicioTemporada= anio

                #Quarters del año q1,q2,q3,q4 [añoInicio , mesInicio, añoFin , mesFin] 
                quarters = self._get__current_quarter_dates_of_the_season(anioInicioTemporada,ms)
                """
                for quarter in quarters:
                    if mes>=quarter[1] and mes<=quarter[3] and quarter[0]==quarter[2]:
                        anioInicial=quarter[0]
                        mesInicial=quarter[1]
                        anioFinal=quarter[2]
                        mesFinal=quarter[3]
                    if mes>=quarter[1] and mes<=quarter[3] and quarter[0]==quarter[2]:
                """
                _logger.error("------------------Trismester method  > "+str(quarters)+" <-----------------------")
                
            elif con.option == "season":
                start_date = con.season_start_month
                end_date = con.season_end_month
        
        if anioInicial=="" or mesInicial =="" or anioFinal=="" or mesFinal=="":
            anioInicial= anio
            mesInicial= mes
            anioFinal= anio
            mesFinal= mes
        
        diaInicial = 1
        diaFinal = self.number_of_days_in_month(anioFinal, mesFinal)

        start_date = str(anioInicial)+"-"+str(mesInicial)+"-"+str(diaInicial)
        end_date = str(anioFinal)+"-"+str(mesFinal)+"-"+str(diaFinal)
        return [start_date, end_date]
    
    def _get__current_quarter_dates_of_the_season(self, anioInicialTemporada, mesInicialTemporada):
        
        today=datetime.today()
        #today=datetime.strptime("2022-12-01", '%Y-%m-%d').date()
        aIQ=anioInicialTemporada
        mIQ= mesInicialTemporada
        aFQ= aIQ + 1 if mIQ + 2 >12 else aIQ
        mFQ=mIQ-10 if mIQ + 2 > 12 else mIQ+2

        isThisQuarter=False

        try:
            while not isThisQuarter:

                if today.month >= mIQ and today.month <= mFQ and today.year == aIQ and today.year==aFQ:
                    isThisQuarter= True
                    _logger.error("--------SUCCESS - TIPO DE PERIODO 1--------------------")
                elif today.month < mIQ and today.month <= mFQ and today.year > aIQ and today.year==aFQ:
                    isThisQuarter= True
                    _logger.error("--------SUCCESS - TIPO DE PERIODO 2--------------------")

                elif today.month >= mIQ and today.month > mFQ and today.year == aIQ and today.year<aFQ:
                    isThisQuarter= True
                    _logger.error("--------SUCCESS - TIPO DE PERIODO 3--------------------")

                else:
                    aIQ= aIQ+1 if mIQ+3>12 else aIQ
                    mIQ= mIQ-9 if mIQ + 3 > 12 else mIQ+3
                    aFQ= aFQ + 1 if mFQ + 3 >12 else aFQ
                    mFQ=mFQ-9 if mFQ + 3 > 12 else mFQ+3
        
        except Exception as e:
            _logger.error("------------------An exception occurred >"+str(e)+"-----------------------")
            

        """
        q1=[]
        q2=[]
        q3=[]
        q4=[]
        
        try:
            
            #Quarters del año [ añoInicio , mesInicio, añoFin , mesFin] 
            q1 = [anio, ms,(anio + 1 if ms + 2 >12 else anio), (ms-10 if ms + 2 > 12 else ms+2)]
            q2 = [(q1[0]+1 if q1[1] + 3 >12 else q1[0]), (q1[1]-9 if q1[1] + 3 > 12 else q1[1]+3), (q1[2]+1 if q1[3]+3 >12 else q1[2]), (q1[3]-9 if q1[3] + 3 > 12 else q1[3]+3)]
            q3 = [(q2[0]+1 if q2[1] + 3 >12 else q2[0]), (q2[1]-9 if q2[1] + 3 > 12 else q2[1]+3), (q2[2]+1 if q2[3]+3 >12 else q2[2]), (q2[3]-9 if q2[3] + 3 > 12 else q2[3]+3)]
            q4 = [(q3[0]+1 if q3[1] + 3 >12 else q3[0]), (q3[1]-9 if q3[1] + 3 > 12 else q3[1]+3), (q3[2]+1 if q3[3]+3 >12 else q3[2]), (q3[3]-9 if q3[3] + 3 > 12 else q3[3]+3)]

  
            #_logger.error("--------SUCCESS - Q1 mes inio ->"+str(q1[1])+"------- Q2 mes inio ->"+str(q2[1])+"----- Q3 mes inio ->"+str(q3[1])+"----- Q4 mes inio ->"+str(q4[1])+"---------------------")
        except Exception as e:
            _logger.error("------------------An exception occurred >"+str(e)+"-----------------------")
            """
        #Fechas de inicio y fin del trimestre actual [ añoInicio , mesInicio, añoFin , mesFin] 
        return [aIQ, mIQ, aFQ, mFQ]

         
        
    """
    def _get_audit_number_goal(self):

        configuration = self.env['paoassignmentauditor.configuration.audit.quantity'].search([])
        
        for con in configuration:
            return ""
    """
    def number_of_days_in_month(self, year, month):
        return monthrange(year, month)[1]


            
                




                