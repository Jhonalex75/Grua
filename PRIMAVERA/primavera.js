import React, { useState, useEffect, useCallback, createContext, useContext, useRef } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from 'firebase/auth';
import { getFirestore, doc, setDoc, getDoc, collection, addDoc, getDocs, query, where, onSnapshot, updateDoc, deleteDoc, writeBatch } from 'firebase/firestore';
import { ChevronDown, ChevronRight, PlusCircle, Edit2, Trash2, Briefcase, Layers, ListChecks, CalendarDays, DollarSign, BarChart3, AlertTriangle, Settings, Eye, ThumbsUp, ThumbsDown, Play, Save, FolderOpen, FileText, Users, GanttChartSquare, TrendingUp, AlertCircle, CheckCircle, Info, ExternalLink, Archive, UserCheck, Target, ShieldAlert, HelpCircle } from 'lucide-react';

// Firebase Configuration
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {
  apiKey: "AIzaSyA3860OlmYf6SJEbBKgqj2o_1dXF0_7IuM",
  authDomain: "ganttify-pro.firebaseapp.com",
  projectId: "ganttify-pro",
  storageBucket: "ganttify-pro.firebasestorage.app",
  messagingSenderId: "515181200682",
  appId: "1:515181200682:web:a45fd0074c5d110b0c0a53"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
// For debugging Firestore issues:
// import { setLogLevel } from "firebase/firestore";
// setLogLevel('debug');


const appId = typeof __app_id !== 'undefined' ? __app_id : 'p6-simulator-enhanced-v1';

// Application Context
const AppContext = createContext();

// --- Date Helper Functions ---
const addDaysToDate = (dateString, days) => {
  if (!dateString) return '';
  const date = new Date(dateString + 'T00:00:00Z'); // Use Z for UTC
  if (isNaN(date.getTime())) return '';
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().split('T')[0];
};

const dateToEpochDays = (dateString) => {
    if (!dateString) return 0;
    const date = new Date(dateString + 'T00:00:00Z');
    if (isNaN(date.getTime())) return 0;
    return Math.floor(date.getTime() / (1000 * 60 * 60 * 24));
};

const dateDiffInDays = (dateStr1, dateStr2) => {
    if (!dateStr1 || !dateStr2) return 0;
    return Math.abs(dateToEpochDays(dateStr1) - dateToEpochDays(dateStr2));
};

const maxDate = (dates) => {
    const validDates = dates.filter(d => d && !isNaN(new Date(d + 'T00:00:00Z').getTime())).map(d => new Date(d + 'T00:00:00Z'));
    if (validDates.length === 0) return null;
    return new Date(Math.max.apply(null, validDates)).toISOString().split('T')[0];
};

const minDate = (dates) => {
    const validDates = dates.filter(d => d && !isNaN(new Date(d + 'T00:00:00Z').getTime())).map(d => new Date(d + 'T00:00:00Z'));
    if (validDates.length === 0) return null;
    return new Date(Math.min.apply(null, validDates)).toISOString().split('T')[0];
};

const formatCurrency = (value) => {
    const number = Number(value);
    if (isNaN(number)) return '$0.00';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(number);
};

const todayDateString = () => new Date().toISOString().split('T')[0];

// --- Main App Component ---
function App() {
  const [userId, setUserId] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false);
  const [currentView, setCurrentView] = useState('home');
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [notification, setNotificationState] = useState({ type: '', message: '', visible: false }); // Consolidated notification state
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [confirmModalProps, setConfirmModalProps] = useState({ message: '', onConfirm: () => {} });

  const setAppNotification = (type, message) => {
    setNotificationState({ type, message, visible: true });
    setTimeout(() => setNotificationState(prev => ({ ...prev, visible: false })), 5000);
  };
  
  const openConfirmationModal = (message, onConfirmAction) => {
    setConfirmModalProps({ message, onConfirm: onConfirmAction });
    setShowConfirmModal(true);
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        setUserId(user.uid);
      } else {
        try {
          if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
            await signInWithCustomToken(auth, __initial_auth_token);
          } else {
            await signInAnonymously(auth);
          }
        } catch (e) { 
          console.error("Error en autenticación:", e); 
          setAppNotification("error", "Error de autenticación.");
        }
      }
      setIsAuthReady(true);
    });
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    if (isAuthReady && userId) {
      setIsLoading(true);
      const projectsColPath = `artifacts/${appId}/users/${userId}/p6_projects`;
      const q = query(collection(db, projectsColPath));
      const unsubscribe = onSnapshot(q, (querySnapshot) => {
        const projectsData = [];
        querySnapshot.forEach((doc) => { projectsData.push({ id: doc.id, ...doc.data() }); });
        setProjects(projectsData.sort((a,b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0) ));
        setIsLoading(false);
      }, (err) => { 
        console.error("Error cargando proyectos:", err); 
        setAppNotification("error", "No se pudieron cargar los proyectos."); 
        setIsLoading(false); 
      });
      return () => unsubscribe();
    }
  }, [isAuthReady, userId]);

  useEffect(() => {
    if (selectedProjectId && userId) {
      setIsLoading(true);
      const projectDocPath = `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`;
      const unsubscribe = onSnapshot(doc(db, projectDocPath), (docSnap) => {
        if (docSnap.exists()) { 
          const projectData = docSnap.data();
          // Ensure default structures for new features
          setSelectedProject({ 
            id: docSnap.id, 
            ...projectData,
            resources: projectData.resources || [],
            risks: projectData.risks || [],
            baselines: projectData.baselines || [],
            activities: (projectData.activities || []).map(act => ({
              ...act,
              assignedResources: act.assignedResources || [],
              budgetedLaborCost: act.budgetedLaborCost || 0,
              budgetedMaterialCost: act.budgetedMaterialCost || 0,
              budgetedNonLaborCost: act.budgetedNonLaborCost || 0, // Renamed from ExpenseCost
              budgetedExpenseCost: act.budgetedExpenseCost || 0, // Keep for compatibility if old data exists
              budgetedResourceCost: act.budgetedResourceCost || 0, // New field for resource costs
              actualLaborCost: act.actualLaborCost || 0,
              actualMaterialCost: act.actualMaterialCost || 0,
              actualNonLaborCost: act.actualNonLaborCost || 0,
              actualExpenseCost: act.actualExpenseCost || 0,
              actualResourceCost: act.actualResourceCost || 0,
            }))
          }); 
        } else { 
          setSelectedProject(null); 
          setSelectedProjectId(null); 
          setAppNotification("info", "El proyecto seleccionado ya no existe.");
        }
        setIsLoading(false);
      }, (err) => { 
        console.error("Error cargando proyecto:", err); 
        setAppNotification("error", "No se pudo cargar el proyecto."); 
        setIsLoading(false); 
      });
      return () => unsubscribe();
    } else { 
      setSelectedProject(null); 
    }
  }, [selectedProjectId, userId]);

  const handleCreateNewProject = async (projectName, projectStartDate) => {
    if (!projectName.trim() || !projectStartDate) { 
      setAppNotification("error", "Nombre y fecha de inicio son obligatorios."); 
      return; 
    }
    if (!userId) { 
      setAppNotification("error", "Usuario no autenticado."); 
      return; 
    }
    setIsLoading(true);
    const newProject = {
      name: projectName, 
      startDate: projectStartDate, 
      createdAt: new Date().toISOString(),
      wbs: [{ id: `wbs-root-${crypto.randomUUID()}`, name: projectName, parentId: null, path: '0' }],
      activities: [], 
      resources: [], // Initialize new fields
      risks: [],
      baselines: [],
      costs: { budgetedTotalCost: 0, actualTotalCost: 0 }, // This might be deprecated if we sum activity costs
      dataDate: projectStartDate,
    };
    try {
      const projectsColPath = `artifacts/${appId}/users/${userId}/p6_projects`;
      const docRef = await addDoc(collection(db, projectsColPath), newProject);
      setSelectedProjectId(docRef.id); 
      setShowNewProjectModal(false); 
      setCurrentView('projectSetup');
      setAppNotification("success", `Proyecto "${projectName}" creado.`);
    } catch (e) { 
      console.error("Error creando proyecto:", e); 
      setAppNotification("error", "Error al crear el proyecto."); 
    }
    finally { setIsLoading(false); }
  };

  const handleSelectProject = (projectId) => { 
    setSelectedProjectId(projectId); 
    setCurrentView('projectSetup'); 
  };
  
  const contextValue = { 
    userId, appId, db, 
    selectedProjectId, selectedProject, 
    isLoading, setIsLoading, 
    notification, setAppNotification,
    setCurrentView, 
    openConfirmationModal,
    projects // Pass projects to context if needed elsewhere, e.g. for EPS
  };

  if (!isAuthReady) return <LoadingSpinner message="Inicializando autenticación..." />;
  
  return (
    <AppContext.Provider value={contextValue}>
      <div className="flex flex-col h-screen font-inter bg-gray-100 text-gray-800">
        <Header />
        <div className="flex flex-1 overflow-hidden">
          <Sidebar currentView={currentView} setCurrentView={setCurrentView} projectSelected={!!selectedProjectId} />
          <main className="flex-1 p-4 md:p-6 overflow-y-auto bg-white shadow-inner m-1 md:m-2 rounded-lg">
            {notification.visible && <Notification type={notification.type} message={notification.message} onClose={() => setNotificationState(prev => ({ ...prev, visible: false }))} />}
            
            {currentView === 'home' && <Home projects={projects} onSelectProject={handleSelectProject} onShowNewProjectModal={() => setShowNewProjectModal(true)} isLoading={isLoading && projects.length === 0} />}
            
            {selectedProjectId && selectedProject && (
              <>
                {currentView === 'projectSetup' && <ProjectSetup />}
                {currentView === 'wbs' && <WBSEditor />}
                {currentView === 'activities' && <ActivityEditor />}
                {currentView === 'schedule' && <SchedulingView />}
                {currentView === 'costs' && <CostsView />}
                {currentView === 'resources' && <ResourceEditor />}
                {currentView === 'risks' && <RiskEditor />}
                {currentView === 'baselines' && <BaselineManager />}
                {currentView === 'progress' && <ProgressTrackingView />} 
                {(['reports', 'layouts'].includes(currentView)) && <PlaceholderView viewName={currentView} />}
              </>
            )}
            {!selectedProjectId && currentView !== 'home' && (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <FolderOpen size={50} className="text-gray-400 mb-4" />
                <p className="text-xl text-gray-600">Por favor, selecciona o crea un proyecto.</p>
                <button onClick={() => setCurrentView('home')} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Ir a Inicio</button>
              </div>
            )}
          </main>
        </div>
        {showNewProjectModal && <NewProjectModal onClose={() => setShowNewProjectModal(false)} onCreate={handleCreateNewProject} />}
        {showConfirmModal && <ConfirmModal 
                                message={confirmModalProps.message} 
                                onConfirm={() => { confirmModalProps.onConfirm(); setShowConfirmModal(false);}} 
                                onCancel={() => setShowConfirmModal(false)} 
                              />}
      </div>
    </AppContext.Provider>
  );
}

// --- UI Components (Header, Sidebar, Home, Modals) ---
const Header = () => {
  const { userId } = useContext(AppContext);
  return (
    <header className="bg-gray-800 text-white p-3 md:p-4 flex justify-between items-center shadow-md print:hidden">
      <div className="flex items-center space-x-2">
        <GanttChartSquare size={28} className="text-blue-400"/>
        <h1 className="text-xl md:text-2xl font-semibold">Simulador P6 Avanzado</h1>
      </div>
      {userId && <div className="text-xs bg-gray-700 px-2 py-1 rounded" title={userId}>UID: ...{userId.slice(-6)}</div>}
    </header>
  );
};

const Sidebar = ({ currentView, setCurrentView, projectSelected }) => {
  const { setAppNotification } = useContext(AppContext);
  const navItems = [
    { id: 'home', label: 'Inicio', icon: FolderOpen, requiresProject: false },
    { id: 'projectSetup', label: 'Proyecto', icon: Settings, requiresProject: true },
    { id: 'wbs', label: 'EDT (WBS)', icon: Layers, requiresProject: true },
    { id: 'activities', label: 'Actividades', icon: ListChecks, requiresProject: true },
    { id: 'resources', label: 'Recursos', icon: Users, requiresProject: true },
    { id: 'schedule', label: 'Programación', icon: CalendarDays, requiresProject: true },
    { id: 'progress', label: 'Avance', icon: TrendingUp, requiresProject: true },
    { id: 'costs', label: 'Costos', icon: DollarSign, requiresProject: true },
    { id: 'risks', label: 'Riesgos', icon: AlertTriangle, requiresProject: true },
    { id: 'baselines', label: 'Líneas Base', icon: Archive, requiresProject: true },
    { id: 'reports', label: 'Informes', icon: BarChart3, requiresProject: true, soon: true },
  ];

  return (
    <aside className="w-20 md:w-64 bg-gray-700 text-gray-200 p-2 md:p-4 space-y-1 md:space-y-2 overflow-y-auto print:hidden">
      {navItems.map(item => (
        <button
          key={item.id}
          title={item.label}
          onClick={() => {
            if (!item.requiresProject || projectSelected) {
              if (item.soon) {
                setAppNotification("info", `La sección "${item.label}" estará disponible pronto.`);
              } else {
                setCurrentView(item.id);
              }
            } else {
              setAppNotification("warning", "Por favor, selecciona o crea un proyecto primero.");
            }
          }}
          disabled={(item.requiresProject && !projectSelected) || item.soon}
          className={`w-full flex items-center space-x-0 md:space-x-3 p-2 md:p-2.5 rounded-md text-left
            ${currentView === item.id ? 'bg-blue-600 text-white shadow-md' : 'hover:bg-gray-600'}
            ${(item.requiresProject && !projectSelected) || item.soon ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <item.icon size={20} className="flex-shrink-0" />
          <span className="hidden md:inline truncate">{item.label}</span>
          {item.soon && <span className="hidden md:inline ml-auto text-xs bg-yellow-500 text-yellow-900 px-1.5 py-0.5 rounded">Pronto</span>}
        </button>
      ))}
    </aside>
  );
};

const Home = ({ projects, onSelectProject, onShowNewProjectModal, isLoading }) => {
 return (
  <div className="p-2">
    <div className="flex justify-between items-center mb-4">
      <h2 className="text-xl md:text-2xl font-semibold text-gray-700">Mis Proyectos</h2>
      <button
        onClick={onShowNewProjectModal}
        className="px-3 py-1.5 md:px-4 md:py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors flex items-center space-x-2 text-sm md:text-base"
      >
        <PlusCircle size={18} />
        <span>Nuevo Proyecto</span>
      </button>
    </div>
    {isLoading && <LoadingSpinner message="Cargando proyectos..." />}
    {!isLoading && projects.length === 0 && (
      <div className="text-center py-10">
        <Briefcase size={48} className="mx-auto text-gray-400 mb-3" />
        <p className="text-gray-500">No hay proyectos aún. ¡Crea uno para comenzar!</p>
      </div>
    )}
    {!isLoading && projects.length > 0 && (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map(project => (
          <div key={project.id} 
               className="p-4 bg-white border border-gray-200 rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer flex flex-col justify-between"
               onClick={() => onSelectProject(project.id)}>
            <div>
              <h3 className="text-md font-medium text-blue-600 truncate" title={project.name}>{project.name}</h3>
              <p className="text-xs text-gray-500 mt-1">Inicio: {project.startDate ? new Date(project.startDate + 'T00:00:00Z').toLocaleDateString() : 'N/A'}</p>
              <p className="text-xs text-gray-400">ID: ...{project.id.slice(-6)}</p>
            </div>
            <div className="mt-3 text-right">
                <ExternalLink size={16} className="text-blue-500 inline-block"/>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);
};

const NewProjectModal = ({ onClose, onCreate }) => {
  const [projectName, setProjectName] = useState('');
  const [projectStartDate, setProjectStartDate] = useState(todayDateString());

  const handleSubmit = (e) => {
    e.preventDefault();
    onCreate(projectName, projectStartDate);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50 print:hidden">
      <div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 className="text-lg md:text-xl font-semibold mb-4 text-gray-800">Crear Nuevo Proyecto</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="projectName" className="block text-sm font-medium text-gray-700 mb-1">Nombre del Proyecto</label>
            <input type="text" id="projectName" value={projectName} onChange={(e) => setProjectName(e.target.value)} className="w-full input-style" required />
          </div>
          <div className="mb-5">
            <label htmlFor="projectStartDate" className="block text-sm font-medium text-gray-700 mb-1">Fecha de Inicio</label>
            <input type="date" id="projectStartDate" value={projectStartDate} onChange={(e) => setProjectStartDate(e.target.value)} className="w-full input-style" required />
          </div>
          <div className="flex justify-end space-x-3">
            <button type="button" onClick={onClose} className="px-4 py-2 btn-secondary text-sm">Cancelar</button>
            <button type="submit" className="px-4 py-2 btn-primary text-sm">Crear Proyecto</button>
          </div>
        </form>
      </div>
    </div>
  );
};

const ConfirmModal = ({ message, onConfirm, onCancel }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-[100] print:hidden">
      <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
        <div className="flex items-center mb-4">
          <AlertTriangle size={24} className="text-yellow-500 mr-3" />
          <h3 className="text-lg font-semibold text-gray-800">Confirmación</h3>
        </div>
        <p className="text-gray-700 mb-6 text-sm">{message}</p>
        <div className="flex justify-end space-x-3">
          <button onClick={onCancel} className="btn-secondary px-4 py-2 text-sm">Cancelar</button>
          <button onClick={onConfirm} className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm">Confirmar</button>
        </div>
      </div>
    </div>
  );
};


const ProjectSetup = () => {
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setAppNotification, setCurrentView, openConfirmationModal } = useContext(AppContext);
  const [projectName, setProjectName] = useState('');
  const [projectStartDate, setProjectStartDate] = useState('');
  const [dataDate, setDataDate] = useState('');

  useEffect(() => {
    if (selectedProject) {
      setProjectName(selectedProject.name || '');
      setProjectStartDate(selectedProject.startDate ? selectedProject.startDate.split('T')[0] : '');
      setDataDate(selectedProject.dataDate ? selectedProject.dataDate.split('T')[0] : (selectedProject.startDate ? selectedProject.startDate.split('T')[0] : ''));
    }
  }, [selectedProject]);

  const handleSaveChanges = async () => {
    if (!selectedProjectId || !userId) { setAppNotification("error", "Error: Proyecto/Usuario no válido."); return; }
    if (!projectName.trim() || !projectStartDate || !dataDate) { setAppNotification("error", "Nombre, Fecha de Inicio y Data Date son obligatorios."); return; }
    setIsLoading(true);
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    try {
      await updateDoc(projectDocRef, { name: projectName, startDate: projectStartDate, dataDate: dataDate });
      setAppNotification("success", "Cambios guardados en la configuración del proyecto.");
    } catch (e) { console.error("Error guardando proyecto:", e); setAppNotification("error", "Error al guardar cambios del proyecto."); }
    finally { setIsLoading(false); }
  };

  const handleDeleteProject = () => {
    if (!selectedProjectId || !userId) { setAppNotification("error", "No hay proyecto para eliminar."); return; }
    openConfirmationModal(
      `¿Estás seguro de que quieres eliminar el proyecto "${selectedProject?.name}" permanentemente? Esta acción es irreversible y eliminará todos los datos asociados (EDT, actividades, etc.).`,
      async () => {
        setIsLoading(true);
        const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
        try {
          await deleteDoc(projectDocRef); 
          setAppNotification("success", `Proyecto "${selectedProject?.name}" eliminado.`); 
          setCurrentView('home');
        } catch (e) { console.error("Error eliminando proyecto:", e); setAppNotification("error", "Error al eliminar proyecto."); }
        finally { setIsLoading(false); }
      }
    );
  };
  
  if (!selectedProject) return <LoadingSpinner message="Cargando configuración del proyecto..." />;

  return (
    <div className="p-1 md:p-4">
      <h2 className="text-xl md:text-2xl font-semibold mb-5 text-gray-800 border-b pb-2">Configuración: {selectedProject.name}</h2>
      <div className="space-y-4 max-w-md">
        <div><label htmlFor="setupProjectName" className="lbl">Nombre Proyecto</label><input type="text" id="setupProjectName" value={projectName} onChange={(e) => setProjectName(e.target.value)} className="w-full input-style"/></div>
        <div><label htmlFor="setupProjectStartDate" className="lbl">Fecha Inicio Proyecto</label><input type="date" id="setupProjectStartDate" value={projectStartDate} onChange={(e) => setProjectStartDate(e.target.value)} className="w-full input-style"/></div>
        <div><label htmlFor="setupDataDate" className="lbl">Data Date (Fecha de Estado)</label><input type="date" id="setupDataDate" value={dataDate} onChange={(e) => setDataDate(e.target.value)} className="w-full input-style"/></div>
        <button onClick={handleSaveChanges} className="btn-primary px-4 py-2 text-sm flex items-center space-x-2"><Save size={18} /> <span>Guardar Cambios</span></button>
        
        <div className="mt-8 pt-4 border-t">
            <h3 className="text-md font-semibold text-red-600 mb-2">Zona de Peligro</h3>
            <button onClick={handleDeleteProject} className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm flex items-center space-x-2"><Trash2 size={18} /> <span>Eliminar Proyecto</span></button>
            <p className="text-xs text-gray-500 mt-1">Esta acción es irreversible.</p>
        </div>
      </div>
    </div>
  );
};

const WBSEditor = () => {
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setAppNotification, openConfirmationModal } = useContext(AppContext);
  const [wbsItems, setWbsItems] = useState([]);
  const [showAddWBSModal, setShowAddWBSModal] = useState(false);
  const [editingWBS, setEditingWBS] = useState(null);
  const [newWBSName, setNewWBSName] = useState('');
  const [selectedParentWBS, setSelectedParentWBS] = useState(null); // Stores parent ID for new WBS

  useEffect(() => {
    if (selectedProject && selectedProject.wbs) {
      const sortedWBS = [...selectedProject.wbs].sort((a, b) => (a.path && b.path) ? a.path.localeCompare(b.path, undefined, { numeric: true, sensitivity: 'base' }) : 0);
      setWbsItems(sortedWBS);
    } else { setWbsItems([]); }
  }, [selectedProject]);

  const getWBSPath = (parentId, currentWbsItems) => {
    const siblings = currentWbsItems.filter(w => w.parentId === parentId);
    const nextSiblingIndex = siblings.length; // Path is 0-indexed for siblings initially

    if (!parentId) { // Root element
        // Find the highest existing root index
        const rootItems = currentWbsItems.filter(w => !w.parentId);
        let maxRootIndex = -1;
        rootItems.forEach(item => {
            const itemIndex = parseInt(item.path.split('.')[0], 10);
            if (!isNaN(itemIndex) && itemIndex > maxRootIndex) {
                maxRootIndex = itemIndex;
            }
        });
        return String(maxRootIndex + 1);
    }
    
    const parent = currentWbsItems.find(w => w.id === parentId);
    if (!parent || typeof parent.path === 'undefined') { 
        console.warn("Parent WBS path not found for parentId:", parentId, "Assigning a temporary path.");
        // Fallback for orphaned items or if parent path is missing
        return `errPath.${Date.now()}.${siblings.length}`; 
    }
    return `${parent.path}.${nextSiblingIndex}`;
  };


  const handleAddOrUpdateWBS = async () => {
    if (!newWBSName.trim()) { setAppNotification("error", "Nombre del elemento EDT es obligatorio."); return; }
    if (!selectedProjectId || !userId) { setAppNotification("error", "Error: Proyecto/Usuario no válido."); return; }
    setIsLoading(true);
    
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    let updatedWBSItems;

    if (editingWBS) {
      updatedWBSItems = wbsItems.map(w => w.id === editingWBS.id ? { ...w, name: newWBSName } : w);
    } else {
      const newPath = getWBSPath(selectedParentWBS, wbsItems);
      updatedWBSItems = [...wbsItems, { id: `wbs-${crypto.randomUUID()}`, name: newWBSName, parentId: selectedParentWBS, path: newPath }];
    }
    
    // Re-sort based on path to ensure correct display order
    updatedWBSItems.sort((a, b) => (a.path && b.path) ? a.path.localeCompare(b.path, undefined, { numeric: true, sensitivity: 'base' }) : 0);

    try {
      await updateDoc(projectDocRef, { wbs: updatedWBSItems });
      setShowAddWBSModal(false); setNewWBSName(''); setEditingWBS(null); setSelectedParentWBS(null);
      setAppNotification("success", `Elemento EDT ${editingWBS ? 'actualizado' : 'añadido'}.`);
    } catch (e) { console.error("Error guardando EDT:", e); setAppNotification("error", "Error al guardar elemento EDT."); } 
    finally { setIsLoading(false); }
  };

  const handleDeleteWBS = (wbsIdToDelete) => {
    openConfirmationModal(
      "¿Estás seguro de que quieres eliminar este elemento EDT? Esto también eliminará todos sus elementos EDT descendientes y las actividades asociadas. Esta acción es irreversible.",
      async () => {
        if (!selectedProjectId || !userId) { setAppNotification("error", "Error: Proyecto/Usuario no válido."); return; }
        setIsLoading(true);
        const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
        
        const getDescendantIds = (parentId, allWbs) => { 
          let ids = []; 
          const children = allWbs.filter(w => w.parentId === parentId); 
          for (const child of children) { ids.push(child.id); ids = ids.concat(getDescendantIds(child.id, allWbs));} 
          return ids; 
        };

        const idsToDelete = [wbsIdToDelete, ...getDescendantIds(wbsIdToDelete, wbsItems)];
        const remainingWBSItems = wbsItems.filter(w => !idsToDelete.includes(w.id));
        const remainingActivities = (selectedProject.activities || []).filter(act => !idsToDelete.includes(act.wbsId));
        
        try {
          await updateDoc(projectDocRef, { wbs: remainingWBSItems, activities: remainingActivities }); 
          setAppNotification("success", "Elemento EDT y sus asociados eliminados.");
        } catch (e) { console.error("Error eliminando WBS:", e); setAppNotification("error", "Error al eliminar EDT."); } 
        finally { setIsLoading(false); }
      }
    );
  };

  const openAddModal = (parentId = null) => { 
    setEditingWBS(null); 
    setNewWBSName(''); 
    // If no parentId is provided, and there's a root WBS, set the root WBS as parent by default.
    // Otherwise, it's a new root element.
    const rootWbsElement = wbsItems.find(w => !w.parentId);
    setSelectedParentWBS(parentId !== null ? parentId : (rootWbsElement ? rootWbsElement.id : null)); 
    setShowAddWBSModal(true); 
  };
  const openEditModal = (wbsItem) => { 
    setEditingWBS(wbsItem); 
    setNewWBSName(wbsItem.name); 
    setSelectedParentWBS(wbsItem.parentId); // Parent doesn't change on edit name
    setShowAddWBSModal(true); 
  };

  const renderWBSNode = (parentId = null, level = 0) => {
    return wbsItems
      .filter(item => item.parentId === parentId)
      .sort((a,b) => (a.path && b.path) ? a.path.localeCompare(b.path, undefined, { numeric: true, sensitivity: 'base' }) : 0) // Ensure consistent sort for rendering
      .map(item => (
        <div key={item.id} style={{ marginLeft: `${level * 20}px` }} className="my-1.5">
          <div className="flex items-center justify-between p-2.5 bg-gray-50 border rounded-md hover:bg-gray-100">
            <span className="text-sm text-gray-700 flex items-center">
              {level > 0 && <ChevronRight size={14} className="mr-1 text-gray-400"/>}
              {item.name} 
              <span className="ml-2 text-xs text-gray-400">(ID: ...{item.id.slice(-4)}, Path: {item.path})</span>
            </span>
            <div className="space-x-1.5">
              <button onClick={() => openAddModal(item.id)} title="Añadir Elemento Hijo" className="p-1 text-green-600 hover:text-green-800"><PlusCircle size={17}/></button>
              <button onClick={() => openEditModal(item)} title="Editar Nombre" className="p-1 text-blue-600 hover:text-blue-800"><Edit2 size={17}/></button>
              <button onClick={() => handleDeleteWBS(item.id)} title="Eliminar Elemento y Descendientes" className="p-1 text-red-600 hover:text-red-800"><Trash2 size={17}/></button>
            </div>
          </div>
          {renderWBSNode(item.id, level + 1)}
        </div>
      ));
  };

  if (!selectedProject) return <LoadingSpinner message="Cargando EDT..." />;
  return (
    <div className="p-1 md:p-4">
      <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
        <h2 className="text-xl md:text-2xl font-semibold text-gray-800">EDT / WBS: {selectedProject.name}</h2>
        <button 
            onClick={() => openAddModal(null)} // Add to root level
            className="btn-primary px-3 py-1.5 md:px-4 md:py-2 text-sm flex items-center space-x-2">
            <PlusCircle size={18} /> <span>Añadir Elemento Raíz</span>
        </button>
      </div>
      {wbsItems.length === 0 && <Notification type="info" message="No hay elementos EDT en este proyecto. Comienza añadiendo un elemento raíz." />}
      <div>{renderWBSNode(null)}</div>
      
      {showAddWBSModal && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50">
          <div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-md">
            <h3 className="text-lg md:text-xl font-semibold mb-4">{editingWBS ? 'Editar' : 'Añadir'} Elemento EDT</h3>
            <form onSubmit={(e) => { e.preventDefault(); handleAddOrUpdateWBS(); }}>
              <div className="mb-4">
                <label htmlFor="wbsName" className="lbl">Nombre del Elemento EDT</label>
                <input type="text" id="wbsName" value={newWBSName} onChange={(e) => setNewWBSName(e.target.value)} className="w-full input-style" required />
              </div>
              {!editingWBS && (
                <p className="text-xs text-gray-600 mb-4">
                  Padre: {selectedParentWBS ? (wbsItems.find(w => w.id === selectedParentWBS)?.name || 'Desconocido') : 'Elemento Raíz (Nivel Superior)'}
                </p>
              )}
              <div className="flex justify-end space-x-3">
                <button type="button" onClick={() => { setShowAddWBSModal(false); setEditingWBS(null); setSelectedParentWBS(null); }} className="btn-secondary px-4 py-2 text-sm">Cancelar</button>
                <button type="submit" className="btn-primary px-4 py-2 text-sm">{editingWBS ? 'Guardar Cambios' : 'Añadir Elemento'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};


const ActivityEditor = () => {
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setAppNotification, openConfirmationModal } = useContext(AppContext);
  const [activities, setActivities] = useState([]);
  const [wbsOptions, setWbsOptions] = useState([]);
  const [resourceOptions, setResourceOptions] = useState([]);
  const [allActivitiesOptions, setAllActivitiesOptions] = useState([]);
  const [showActivityModal, setShowActivityModal] = useState(false);
  const [currentActivity, setCurrentActivity] = useState(null); // Stores the activity being edited

  const initialFormState = {
    id: '', name: '', wbsId: '', duration: 1, predecessors: [], 
    assignedResources: [], // [{ resourceId: '', budgetedUnits: 0 }]
    percentComplete: 0,
    actualStartDate: '', actualFinishDate: '',
    budgetedLaborCost: 0, budgetedMaterialCost: 0, budgetedNonLaborCost: 0, budgetedResourceCost: 0, budgetedTotalCost: 0,
    actualLaborCost: 0, actualMaterialCost: 0, actualNonLaborCost: 0, actualResourceCost: 0, actualTotalCost: 0,
    es: '', ef: '', ls: '', lf: '', float: null, isCritical: false,
  };
  const [activityFormData, setActivityFormData] = useState(initialFormState);

  useEffect(() => {
    if (selectedProject) {
      const projectActivities = (selectedProject.activities || []).map(act => {
        const budgetedResourceCost = (act.assignedResources || []).reduce((sum, assign) => {
            const resource = selectedProject.resources.find(r => r.id === assign.resourceId);
            return sum + ((assign.budgetedUnits || 0) * (resource?.costRate || 0));
        }, 0);
        const actualResourceCost = (act.assignedResources || []).reduce((sum, assign) => {
            const resource = selectedProject.resources.find(r => r.id === assign.resourceId);
            return sum + ((assign.actualUnits || 0) * (resource?.costRate || 0));
        },0);

        return {
          ...act,
          budgetedLaborCost: act.budgetedLaborCost || 0,
          budgetedMaterialCost: act.budgetedMaterialCost || 0,
          budgetedNonLaborCost: act.budgetedNonLaborCost || 0,
          budgetedResourceCost: budgetedResourceCost,
          budgetedTotalCost: (act.budgetedLaborCost || 0) + (act.budgetedMaterialCost || 0) + (act.budgetedNonLaborCost || 0) + budgetedResourceCost,
          actualLaborCost: act.actualLaborCost || 0,
          actualMaterialCost: act.actualMaterialCost || 0,
          actualNonLaborCost: act.actualNonLaborCost || 0,
          actualResourceCost: actualResourceCost,
          actualTotalCost: (act.actualLaborCost || 0) + (act.actualMaterialCost || 0) + (act.actualNonLaborCost || 0) + actualResourceCost,
          assignedResources: act.assignedResources || [],
          actualStartDate: act.actualStartDate || '',
          actualFinishDate: act.actualFinishDate || '',
        };
      });
      setActivities(projectActivities.sort((a, b) => (a.id > b.id ? 1 : -1)));
      
      const wbsOpts = (selectedProject.wbs || []).map(w => ({ value: w.id, label: `${w.path} - ${w.name}`, path: w.path })).sort((a,b) => (a.path && b.path) ? a.path.localeCompare(b.path, undefined, { numeric: true, sensitivity: 'base' }) : 0);
      setWbsOptions(wbsOpts);

      const resOpts = (selectedProject.resources || []).map(r => ({ value: r.id, label: `${r.name} (${r.type})`}));
      setResourceOptions(resOpts);
      
      setAllActivitiesOptions(projectActivities.map(act => ({ value: act.id, label: `${act.id.slice(0,8)}... - ${act.name}` })));
      
      if (wbsOpts.length > 0 && !activityFormData.wbsId) {
        setActivityFormData(prev => ({ ...prev, wbsId: wbsOpts[0].value }));
      }
    }
  }, [selectedProject, activityFormData.wbsId]); // Added activityFormData.wbsId dependency

  const calculateActivityCosts = (formData) => {
    const updatedForm = { ...formData };
    const budgetedResourceCostTotal = (updatedForm.assignedResources || []).reduce((sum, assign) => {
        const resource = resourceOptions.find(r => r.value === assign.resourceId); // Use resourceOptions for costRate
        const resDetails = selectedProject.resources.find(r => r.id === assign.resourceId);
        return sum + ((assign.budgetedUnits || 0) * (resDetails?.costRate || 0));
    }, 0);
    updatedForm.budgetedResourceCost = budgetedResourceCostTotal;
    updatedForm.budgetedTotalCost = (updatedForm.budgetedLaborCost || 0) + (updatedForm.budgetedMaterialCost || 0) + (updatedForm.budgetedNonLaborCost || 0) + budgetedResourceCostTotal;
    
    // Similar for actual costs if actualUnits are tracked on assignments
    const actualResourceCostTotal = (updatedForm.assignedResources || []).reduce((sum, assign) => {
        const resDetails = selectedProject.resources.find(r => r.id === assign.resourceId);
        return sum + ((assign.actualUnits || 0) * (resDetails?.costRate || 0));
    },0);
    updatedForm.actualResourceCost = actualResourceCostTotal;
    updatedForm.actualTotalCost = (updatedForm.actualLaborCost || 0) + (updatedForm.actualMaterialCost || 0) + (updatedForm.actualNonLaborCost || 0) + actualResourceCostTotal;
    return updatedForm;
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    let parsedValue = type === 'checkbox' ? checked : (name.toLowerCase().includes('cost') || name === 'duration' || name === 'percentComplete' ? parseFloat(value) || 0 : value);
    
    setActivityFormData(prev => {
      let updatedForm = { ...prev, [name]: parsedValue };
      // Auto-update dates based on percentComplete
      if (name === 'percentComplete') {
        if (parsedValue > 0 && parsedValue < 100 && !updatedForm.actualStartDate) {
          updatedForm.actualStartDate = selectedProject?.dataDate || todayDateString();
        } else if (parsedValue === 100 && !updatedForm.actualFinishDate) {
          updatedForm.actualFinishDate = selectedProject?.dataDate || todayDateString();
          if (!updatedForm.actualStartDate) updatedForm.actualStartDate = selectedProject?.dataDate || todayDateString(); // Ensure start date is also set
        } else if (parsedValue === 0) {
          // Optionally clear actual dates if progress reset to 0, or leave as is.
          // updatedForm.actualStartDate = '';
          // updatedForm.actualFinishDate = '';
        }
      }
      return calculateActivityCosts(updatedForm);
    });
  };

  const handlePredecessorChange = (selectedOptions) => {
    setActivityFormData(prev => ({ ...prev, predecessors: Array.from(selectedOptions).map(option => option.value) }));
  };

  const handleResourceAssignmentChange = (index, field, value) => {
    setActivityFormData(prev => {
        const updatedAssignments = [...prev.assignedResources];
        updatedAssignments[index] = { ...updatedAssignments[index], [field]: field === 'budgetedUnits' ? parseFloat(value) || 0 : value };
        const newForm = {...prev, assignedResources: updatedAssignments};
        return calculateActivityCosts(newForm);
    });
  };

  const addResourceAssignment = () => {
    setActivityFormData(prev => {
      const newAssignment = { resourceId: resourceOptions.length > 0 ? resourceOptions[0].value : '', budgetedUnits: 0 };
      const newForm = {...prev, assignedResources: [...prev.assignedResources, newAssignment]};
      return calculateActivityCosts(newForm);
    });
  };

  const removeResourceAssignment = (index) => {
    setActivityFormData(prev => {
      const updatedAssignments = prev.assignedResources.filter((_, i) => i !== index);
      const newForm = {...prev, assignedResources: updatedAssignments};
      return calculateActivityCosts(newForm);
    });
  };


  const handleOpenModal = (activity = null) => {
    setCurrentActivity(activity);
    if (activity) {
      // Ensure all fields from initialFormState are present, then override with activity data
      const populatedActivityData = { ...initialFormState, ...activity };
      setActivityFormData(calculateActivityCosts(populatedActivityData));
    } else {
      const newId = `act-${crypto.randomUUID()}`;
      const defaultWbs = wbsOptions.length > 0 ? wbsOptions[0].value : '';
      setActivityFormData(calculateActivityCosts({ ...initialFormState, id: newId, wbsId: defaultWbs }));
    }
    setShowActivityModal(true);
  };

  const handleSaveActivity = async () => {
    if (!activityFormData.name.trim() || !activityFormData.wbsId) { setAppNotification("error", "Nombre de actividad y elemento EDT son obligatorios."); return; }
    if (!selectedProjectId || !userId) { setAppNotification("error", "Error: Proyecto/Usuario no válido."); return; }
    setIsLoading(true);
    
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    
    // Exclude purely calculated schedule fields that should be re-calculated by CPM
    const { es, ef, ls, lf, float, isCritical, ...dataToSave } = activityFormData; 
    
    // Persist existing schedule data if available, or set to null/defaults if not
    const activityToPersist = { 
        ...dataToSave, 
        es: currentActivity?.es || null, 
        ef: currentActivity?.ef || null, 
        ls: currentActivity?.ls || null, 
        lf: currentActivity?.lf || null, 
        float: currentActivity?.float !== undefined ? currentActivity.float : null, 
        isCritical: currentActivity?.isCritical || false 
    };

    let updatedActivities;
    if (currentActivity) { // Editing existing activity
      updatedActivities = activities.map(act => act.id === currentActivity.id ? activityToPersist : act);
    } else { // Adding new activity
      updatedActivities = [...activities, activityToPersist];
    }

    try {
      await updateDoc(projectDocRef, { activities: updatedActivities });
      setShowActivityModal(false); 
      setCurrentActivity(null);
      setAppNotification("success", `Actividad "${activityFormData.name}" ${currentActivity ? 'actualizada' : 'añadida'}.`);
    } catch (e) { 
      console.error("Error guardando actividad:", e); 
      setAppNotification("error", "Error al guardar la actividad."); 
    } finally { 
      setIsLoading(false); 
    }
  };

  const handleDeleteActivity = (activityIdToDelete, activityName) => { 
    openConfirmationModal(
      `¿Estás seguro de que quieres eliminar la actividad "${activityName}" (ID: ...${activityIdToDelete.slice(-6)})? Esta acción es irreversible.`,
      async () => {
        if (!selectedProjectId || !userId) { setAppNotification("error", "Error: Proyecto/Usuario no válido."); return; }
        setIsLoading(true);
        const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
        const remainingActivities = activities
          .filter(act => act.id !== activityIdToDelete)
          .map(act => ({ ...act, predecessors: (act.predecessors || []).filter(pId => pId !== activityIdToDelete) }));
        try { 
          await updateDoc(projectDocRef, { activities: remainingActivities }); 
          setAppNotification("success", `Actividad "${activityName}" eliminada.`);
        }
        catch (e) { console.error("Error eliminando actividad:", e); setAppNotification("error", "Error al eliminar la actividad."); } 
        finally { setIsLoading(false); }
      }
    );
  };
  
  const getWBSName = (wbsId) => wbsOptions.find(w => w.value === wbsId)?.label || 'N/A';

  if (!selectedProject) return <LoadingSpinner message="Cargando actividades..." />;
  return (
    <div className="p-1 md:p-4">
      <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
        <h2 className="text-xl md:text-2xl font-semibold">Actividades: {selectedProject.name}</h2>
        <button onClick={() => handleOpenModal()} className="btn-primary px-3 py-1.5 md:px-4 md:py-2 text-sm flex items-center space-x-2" disabled={wbsOptions.length === 0}>
          <PlusCircle size={18} /> <span>Añadir Actividad</span>
        </button>
      </div>
      {wbsOptions.length === 0 && <Notification type="warning" message="Debes crear al menos un elemento EDT (WBS) antes de poder añadir actividades." />}
      {activities.length === 0 && wbsOptions.length > 0 && <p className="text-gray-500 py-4 text-center">No hay actividades en este proyecto. ¡Añade la primera!</p>}
      
      {activities.length > 0 && (
        <div className="overflow-x-auto shadow-md rounded-lg">
          <table className="min-w-full bg-white border text-sm">
            <thead className="bg-gray-50">
              <tr>
                {['ID', 'Nombre', 'EDT', 'Dur. (d)', 'Costo Presup. Total', '% Comp.', 'Inicio Real', 'Fin Real', 'Acciones'].map(h => <th key={h} className="th-style">{h}</th>)}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {activities.map(act => (
                <tr key={act.id} className="hover:bg-gray-50">
                  <td className="td-style font-mono text-xs" title={act.id}>{act.id.slice(0,8)}...</td>
                  <td className="td-style">{act.name}</td>
                  <td className="td-style" title={getWBSName(act.wbsId)}>{getWBSName(act.wbsId).length > 25 ? getWBSName(act.wbsId).substring(0,22) + '...' : getWBSName(act.wbsId)}</td>
                  <td className="td-style text-center">{act.duration}</td>
                  <td className="td-style text-right">{formatCurrency(act.budgetedTotalCost)}</td>
                  <td className="td-style text-center">{act.percentComplete || 0}%</td>
                  <td className="td-style text-center">{act.actualStartDate || '-'}</td>
                  <td className="td-style text-center">{act.actualFinishDate || '-'}</td>
                  <td className="td-style space-x-1.5">
                    <button onClick={() => handleOpenModal(act)} title="Editar Actividad" className="btn-icon text-blue-600"><Edit2 size={17}/></button>
                    <button onClick={() => handleDeleteActivity(act.id, act.name)} title="Eliminar Actividad" className="btn-icon text-red-600"><Trash2 size={17}/></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showActivityModal && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-3xl my-8"> {/* Increased max-width */}
            <h3 className="text-lg md:text-xl font-semibold mb-4">{currentActivity ? 'Editar' : 'Añadir'} Actividad (ID: {activityFormData.id.slice(0,8)}...)</h3>
            <form onSubmit={(e) => { e.preventDefault(); handleSaveActivity(); }}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4 mb-4 max-h-[70vh] overflow-y-auto pr-2"> {/* Scrollable content area */}
                {/* General Activity Details */}
                <div><label htmlFor="activityName" className="lbl">Nombre Actividad</label><input type="text" name="name" id="activityName" value={activityFormData.name} onChange={handleInputChange} className="w-full input-style" required /></div>
                <div><label htmlFor="activityWbsId" className="lbl">Elemento EDT (WBS)</label><select name="wbsId" id="activityWbsId" value={activityFormData.wbsId} onChange={handleInputChange} className="w-full input-style" required>{wbsOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select></div>
                <div><label htmlFor="activityDuration" className="lbl">Duración Original (días)</label><input type="number" name="duration" id="activityDuration" value={activityFormData.duration} onChange={handleInputChange} min="0" className="w-full input-style" required /></div>
                
                {/* Progress */}
                <div className="md:col-span-2 mt-2 pt-3 border-t"><h4 className="text-md font-semibold text-gray-700 mb-2">Progreso</h4></div>
                <div><label htmlFor="activityPercentComplete" className="lbl">% Completado</label><input type="number" name="percentComplete" id="activityPercentComplete" value={activityFormData.percentComplete} onChange={handleInputChange} min="0" max="100" step="1" className="w-full input-style" /></div>
                <div><label htmlFor="actualStartDate" className="lbl">Fecha Inicio Real</label><input type="date" name="actualStartDate" id="actualStartDate" value={activityFormData.actualStartDate} onChange={handleInputChange} className="w-full input-style" /></div>
                <div><label htmlFor="actualFinishDate" className="lbl">Fecha Fin Real</label><input type="date" name="actualFinishDate" id="actualFinishDate" value={activityFormData.actualFinishDate} onChange={handleInputChange} className="w-full input-style" /></div>
                
                {/* Budgeted Costs */}
                <div className="md:col-span-2 mt-2 pt-3 border-t"><h4 className="text-md font-semibold text-gray-700 mb-2">Costos Presupuestados Fijos</h4></div>
                <div><label htmlFor="budgetedLaborCost" className="lbl">Mano de Obra Fija ($)</label><input type="number" name="budgetedLaborCost" value={activityFormData.budgetedLaborCost} onChange={handleInputChange} min="0" step="any" className="w-full input-style" /></div>
                <div><label htmlFor="budgetedMaterialCost" className="lbl">Materiales Fijos ($)</label><input type="number" name="budgetedMaterialCost" value={activityFormData.budgetedMaterialCost} onChange={handleInputChange} min="0" step="any" className="w-full input-style" /></div>
                <div><label htmlFor="budgetedNonLaborCost" className="lbl">No Mano de Obra/Equipos Fijos ($)</label><input type="number" name="budgetedNonLaborCost" value={activityFormData.budgetedNonLaborCost} onChange={handleInputChange} min="0" step="any" className="w-full input-style" /></div>
                <div><label htmlFor="budgetedResourceCost" className="lbl">Recursos Asignados ($)</label><input type="number" value={activityFormData.budgetedResourceCost} className="w-full input-style bg-gray-100" readOnly /></div>
                <div className="font-semibold"><label className="lbl">Total Presupuestado ($)</label><input type="number" value={activityFormData.budgetedTotalCost} className="w-full input-style bg-gray-100 font-bold" readOnly /></div>

                {/* Resource Assignments */}
                <div className="md:col-span-2 mt-2 pt-3 border-t"><h4 className="text-md font-semibold text-gray-700 mb-2 flex justify-between items-center"><span>Recursos Asignados (Presupuestados)</span> <button type="button" onClick={addResourceAssignment} className="btn-secondary text-xs px-2 py-1"><PlusCircle size={14} className="inline mr-1"/>Añadir Recurso</button></h4></div>
                {activityFormData.assignedResources.map((assign, index) => (
                    <div key={index} className="md:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-2 items-end border p-2 rounded-md">
                        <div><label htmlFor={`resId-${index}`} className="lbl-xs">Recurso</label><select id={`resId-${index}`} value={assign.resourceId} onChange={(e) => handleResourceAssignmentChange(index, 'resourceId', e.target.value)} className="w-full input-style text-xs">{resourceOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select></div>
                        <div><label htmlFor={`resUnits-${index}`} className="lbl-xs">Unidades Presup.</label><input type="number" id={`resUnits-${index}`} value={assign.budgetedUnits} onChange={(e) => handleResourceAssignmentChange(index, 'budgetedUnits', e.target.value)} min="0" className="w-full input-style text-xs" /></div>
                        <button type="button" onClick={() => removeResourceAssignment(index)} className="btn-secondary bg-red-100 hover:bg-red-200 text-red-600 text-xs px-2 py-1 self-end sm:self-center h-8"><Trash2 size={14}/></button>
                    </div>
                ))}
                {activityFormData.assignedResources.length === 0 && <p className="text-xs text-gray-500 md:col-span-2">No hay recursos asignados a esta actividad.</p>}


                {/* Predecessors */}
                <div className="md:col-span-2 mt-2 pt-3 border-t"><label htmlFor="activityPredecessors" className="lbl">Predecesoras (Relación Fin-a-Inicio)</label><select multiple name="predecessors" value={activityFormData.predecessors} onChange={(e) => handlePredecessorChange(e.target.selectedOptions)} className="w-full input-style h-24">{allActivitiesOptions.filter(opt => opt.value !== activityFormData.id).map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select><p className="text-xs text-gray-500 mt-1">Usa Ctrl/Cmd + click para seleccionar múltiples predecesoras.</p></div>
                
                {/* Calculated Schedule Data (Read-only) */}
                {currentActivity && (activityFormData.es || activityFormData.ls) && <div className="md:col-span-2 mt-2 pt-3 border-t"><h4 className="text-md font-semibold text-gray-700 mb-2">Datos de Programación (Calculados)</h4><div className="grid grid-cols-2 md:grid-cols-4 gap-x-6 gap-y-2">
                  <div><label className="lbl-xs">Inicio Temprano (ES)</label><input type="text" value={activityFormData.es||'-'} className="input-xs-ro" readOnly/></div><div><label className="lbl-xs">Fin Temprano (EF)</label><input type="text" value={activityFormData.ef||'-'} className="input-xs-ro" readOnly/></div>
                  <div><label className="lbl-xs">Inicio Tardío (LS)</label><input type="text" value={activityFormData.ls||'-'} className="input-xs-ro" readOnly/></div><div><label className="lbl-xs">Fin Tardío (LF)</label><input type="text" value={activityFormData.lf||'-'} className="input-xs-ro" readOnly/></div>
                  <div><label className="lbl-xs">Holgura Total</label><input type="text" value={activityFormData.float !== null ? activityFormData.float : '-'} className="input-xs-ro" readOnly/></div><div><label className="lbl-xs">Es Crítica</label><input type="text" value={activityFormData.isCritical ? 'Sí':'No'} className="input-xs-ro" readOnly/></div>
                </div></div>}
              </div>
              <div className="flex justify-end space-x-3 mt-5 pt-4 border-t">
                <button type="button" onClick={() => setShowActivityModal(false)} className="btn-secondary px-4 py-2 text-sm">Cancelar</button>
                <button type="submit" className="btn-primary px-4 py-2 text-sm">{currentActivity ? 'Guardar Cambios' : 'Añadir Actividad'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// --- Resource Editor Component ---
const ResourceEditor = () => {
    const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setAppNotification, openConfirmationModal } = useContext(AppContext);
    const [resources, setResources] = useState([]);
    const [showResourceModal, setShowResourceModal] = useState(false);
    const [currentResource, setCurrentResource] = useState(null); // For editing
    const initialResourceForm = { id: '', name: '', type: 'Labor', unit: '', costRate: 0 };
    const [resourceFormData, setResourceFormData] = useState(initialResourceForm);

    const resourceTypes = ['Labor', 'Material', 'NonLabor', 'Equipment'];

    useEffect(() => {
        if (selectedProject && selectedProject.resources) {
            setResources(selectedProject.resources);
        } else {
            setResources([]);
        }
    }, [selectedProject]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setResourceFormData(prev => ({ ...prev, [name]: name === 'costRate' ? parseFloat(value) || 0 : value }));
    };

    const handleOpenModal = (resource = null) => {
        setCurrentResource(resource);
        if (resource) {
            setResourceFormData({ ...initialResourceForm, ...resource });
        } else {
            setResourceFormData({ ...initialResourceForm, id: `res-${crypto.randomUUID()}` });
        }
        setShowResourceModal(true);
    };

    const handleSaveResource = async () => {
        if (!resourceFormData.name.trim() || !resourceFormData.type.trim()) {
            setAppNotification("error", "Nombre y tipo de recurso son obligatorios.");
            return;
        }
        if (!selectedProjectId || !userId) {
            setAppNotification("error", "Error: Proyecto/Usuario no válido.");
            return;
        }
        setIsLoading(true);
        const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
        
        let updatedResources;
        if (currentResource) { // Editing
            updatedResources = resources.map(res => res.id === currentResource.id ? resourceFormData : res);
        } else { // Adding new
            updatedResources = [...resources, resourceFormData];
        }

        try {
            await updateDoc(projectDocRef, { resources: updatedResources });
            setShowResourceModal(false);
            setCurrentResource(null);
            setAppNotification("success", `Recurso "${resourceFormData.name}" ${currentResource ? 'actualizado' : 'añadido'}.`);
        } catch (e) {
            console.error("Error guardando recurso:", e);
            setAppNotification("error", "Error al guardar el recurso.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteResource = (resourceId, resourceName) => {
        // Check if resource is assigned to any activity
        const isAssigned = selectedProject.activities.some(act => 
            (act.assignedResources || []).some(ar => ar.resourceId === resourceId)
        );

        if (isAssigned) {
            setAppNotification("error", `El recurso "${resourceName}" está asignado a una o más actividades y no puede ser eliminado. Primero desasígnelo.`);
            return;
        }

        openConfirmationModal(
            `¿Estás seguro de que quieres eliminar el recurso "${resourceName}" (ID: ...${resourceId.slice(-6)})? Esta acción es irreversible.`,
            async () => {
                if (!selectedProjectId || !userId) { setAppNotification("error", "Error: Proyecto/Usuario no válido."); return; }
                setIsLoading(true);
                const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
                const remainingResources = resources.filter(res => res.id !== resourceId);
                try {
                    await updateDoc(projectDocRef, { resources: remainingResources });
                    setAppNotification("success", `Recurso "${resourceName}" eliminado.`);
                } catch (e) {
                    console.error("Error eliminando recurso:", e);
                    setAppNotification("error", "Error al eliminar el recurso.");
                } finally {
                    setIsLoading(false);
                }
            }
        );
    };

    if (!selectedProject) return <LoadingSpinner message="Cargando recursos..." />;

    return (
        <div className="p-1 md:p-4">
            <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
                <h2 className="text-xl md:text-2xl font-semibold">Recursos del Proyecto: {selectedProject.name}</h2>
                <button onClick={() => handleOpenModal()} className="btn-primary px-3 py-1.5 md:px-4 md:py-2 text-sm flex items-center space-x-2">
                    <PlusCircle size={18} /> <span>Añadir Recurso</span>
                </button>
            </div>

            {resources.length === 0 && <Notification type="info" message="No hay recursos definidos para este proyecto." />}
            
            {resources.length > 0 && (
                <div className="overflow-x-auto shadow-md rounded-lg">
                    <table className="min-w-full bg-white border text-sm">
                        <thead className="bg-gray-50">
                            <tr>{['ID', 'Nombre', 'Tipo', 'Unidad', 'Costo/Unidad', 'Acciones'].map(h => <th key={h} className="th-style">{h}</th>)}</tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {resources.map(res => (
                                <tr key={res.id} className="hover:bg-gray-50">
                                    <td className="td-style font-mono text-xs" title={res.id}>{res.id.slice(0,8)}...</td>
                                    <td className="td-style">{res.name}</td>
                                    <td className="td-style">{res.type}</td>
                                    <td className="td-style">{res.unit || '-'}</td>
                                    <td className="td-style text-right">{formatCurrency(res.costRate)}</td>
                                    <td className="td-style space-x-1.5">
                                        <button onClick={() => handleOpenModal(res)} title="Editar Recurso" className="btn-icon text-blue-600"><Edit2 size={17}/></button>
                                        <button onClick={() => handleDeleteResource(res.id, res.name)} title="Eliminar Recurso" className="btn-icon text-red-600"><Trash2 size={17}/></button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {showResourceModal && (
                <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50">
                    <div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-lg">
                        <h3 className="text-lg md:text-xl font-semibold mb-4">{currentResource ? 'Editar' : 'Añadir'} Recurso</h3>
                        <form onSubmit={(e) => { e.preventDefault(); handleSaveResource(); }}>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                <div><label htmlFor="resourceName" className="lbl">Nombre Recurso</label><input type="text" name="name" id="resourceName" value={resourceFormData.name} onChange={handleInputChange} className="w-full input-style" required /></div>
                                <div><label htmlFor="resourceType" className="lbl">Tipo Recurso</label><select name="type" id="resourceType" value={resourceFormData.type} onChange={handleInputChange} className="w-full input-style" required>{resourceTypes.map(type => <option key={type} value={type}>{type}</option>)}</select></div>
                                <div><label htmlFor="resourceUnit" className="lbl">Unidad (ej: hr, m2, ud)</label><input type="text" name="unit" id="resourceUnit" value={resourceFormData.unit} onChange={handleInputChange} className="w-full input-style" /></div>
                                <div><label htmlFor="resourceCostRate" className="lbl">Costo por Unidad ($)</label><input type="number" name="costRate" id="resourceCostRate" value={resourceFormData.costRate} onChange={handleInputChange} min="0" step="any" className="w-full input-style" /></div>
                            </div>
                            <div className="flex justify-end space-x-3 mt-5">
                                <button type="button" onClick={() => setShowResourceModal(false)} className="btn-secondary px-4 py-2 text-sm">Cancelar</button>
                                <button type="submit" className="btn-primary px-4 py-2 text-sm">{currentResource ? 'Guardar Cambios' : 'Añadir Recurso'}</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};


// --- Basic Gantt Chart Component ---
const BasicGanttChart = ({ activities, projectStartDate, baselines, selectedBaselineId }) => {
  if (!activities || activities.length === 0 || !projectStartDate) {
    return <div className="p-4 text-center text-gray-500">No hay datos suficientes para mostrar la Carta Gantt. Asegúrate de tener actividades programadas y una fecha de inicio del proyecto.</div>;
  }

  const BAR_HEIGHT = 18;
  const PROGRESS_BAR_HEIGHT = 8;
  const BASELINE_BAR_HEIGHT = 10;
  const ROW_GAP = 12;
  const LABEL_WIDTH = 180; 
  const SIDE_PADDING = 20;
  const TOP_PADDING = 60; 
  const DAY_WIDTH = 20; 
  const TICK_HEIGHT = 5;

  const chartActivities = activities.filter(act => act.es && act.ef && (act.duration > 0 || (act.duration === 0 && act.es))); // Include milestones
  
  let baselineActivities = [];
  if (selectedBaselineId && baselines) {
      const selectedBaseline = baselines.find(b => b.id === selectedBaselineId);
      if (selectedBaseline && selectedBaseline.activitiesSnapshot) {
          baselineActivities = selectedBaseline.activitiesSnapshot.filter(act => act.es && act.ef);
      }
  }

  if (chartActivities.length === 0) {
    return <div className="p-4 text-center text-gray-500">No hay actividades con fechas de inicio/fin calculadas para mostrar en la Gantt.</div>;
  }
  
  const allDates = [projectStartDate];
  chartActivities.forEach(act => { allDates.push(act.es, act.ef, act.actualStartDate, act.actualFinishDate); });
  baselineActivities.forEach(act => { allDates.push(act.es, act.ef); });

  const overallStartDate = minDate(allDates.filter(Boolean));
  const overallEndDate = maxDate(allDates.filter(Boolean));

  if (!overallStartDate || !overallEndDate) {
      return <div className="p-4 text-center text-gray-500">No se pudieron determinar las fechas de inicio/fin del gráfico.</div>;
  }

  const totalDays = dateDiffInDays(overallStartDate, overallEndDate) + 1;
  const chartWidth = Math.max(totalDays * DAY_WIDTH, 300); // Min chart width
  const svgWidth = LABEL_WIDTH + chartWidth + SIDE_PADDING * 2;
  const svgHeight = TOP_PADDING + chartActivities.length * (BAR_HEIGHT + ROW_GAP) + SIDE_PADDING;

  const dateToX = (dateStr) => {
    if (!dateStr) return 0;
    const diff = dateDiffInDays(overallStartDate, dateStr);
    return diff * DAY_WIDTH;
  };

  const timelineTicks = [];
  let currentDate = new Date(overallStartDate + 'T00:00:00Z');
  const endDateObj = new Date(overallEndDate + 'T00:00:00Z');
  
  let monthTracker = -1;

  for (let i = 0; i <= totalDays; i++) {
    const xPos = i * DAY_WIDTH;
    const day = currentDate.getUTCDate();
    const month = currentDate.getUTCMonth();
    
    if (day === 1 || i === 0) { 
        timelineTicks.push({
            x: xPos,
            label: currentDate.toLocaleDateString('es-ES', { month: 'short', year: '2-digit', timeZone: 'UTC' }),
            isMonth: true,
        });
        monthTracker = month;
    } else if (totalDays <= 90 && (day % 5 === 0 || day === 1)) { 
        timelineTicks.push({ x: xPos, label: String(day), isMonth: false });
    } else if (totalDays > 90 && (day % 7 === 0 || day === 1 )) { 
        timelineTicks.push({ x: xPos, label: String(day), isMonth: false });
    }
    currentDate.setUTCDate(currentDate.getUTCDate() + 1);
    if (currentDate > endDateObj && i < totalDays) { 
        if (timelineTicks[timelineTicks.length-1].label !== String(endDateObj.getUTCDate())) {
             timelineTicks.push({ x: (i+1) * DAY_WIDTH, label: String(endDateObj.getUTCDate()), isMonth: false });
        }
    }
     if (i >= totalDays && currentDate <= endDateObj) { 
        if (monthTracker !== endDateObj.getUTCMonth()) {
             timelineTicks.push({ x: (i+1) * DAY_WIDTH, label: endDateObj.toLocaleDateString('es-ES', { month: 'short', year: '2-digit', timeZone: 'UTC' }), isMonth: true });
        }
    }
  }

  return (
    <div className="overflow-x-auto bg-white p-2 rounded shadow-lg mt-4 border">
      <svg width={svgWidth} height={svgHeight} className="font-sans text-xs">
        <defs>
          <pattern id="gridPattern" width={DAY_WIDTH} height={BAR_HEIGHT + ROW_GAP} patternUnits="userSpaceOnUse">
            <path d={`M ${DAY_WIDTH} 0 L ${DAY_WIDTH} ${BAR_HEIGHT + ROW_GAP} M 0 ${BAR_HEIGHT + ROW_GAP} L ${DAY_WIDTH} ${BAR_HEIGHT + ROW_GAP}`} fill="none" stroke="rgba(200,200,200,0.2)" strokeWidth="0.5"/>
          </pattern>
           <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{stopColor: 'rgb(34, 197, 94)', stopOpacity: 1}} /> {/* green-500 */}
            <stop offset="100%" style={{stopColor: 'rgb(22, 163, 74)', stopOpacity: 1}} /> {/* green-600 */}
          </linearGradient>
        </defs>

        <rect x={LABEL_WIDTH + SIDE_PADDING} y={TOP_PADDING} width={chartWidth} height={chartActivities.length * (BAR_HEIGHT + ROW_GAP)} fill="url(#gridPattern)" />

        {/* Timeline */}
        <g transform={`translate(${LABEL_WIDTH + SIDE_PADDING}, ${TOP_PADDING})`}>
          <line x1="0" y1="-5" x2={chartWidth} y2="-5" stroke="#ccc" strokeWidth="1"/>
          {timelineTicks.map((tick, index) => (
            <g key={`tick-${index}`} transform={`translate(${tick.x}, 0)`}>
              <line y1="-5" y2={tick.isMonth ? -TICK_HEIGHT - 8 : -TICK_HEIGHT} stroke="#888" strokeWidth="0.5" />
              <text y={tick.isMonth ? -22 : -12} x="3" textAnchor="start" fontSize="0.65rem" fill="#555" className={tick.isMonth ? 'font-semibold': ''}>
                {tick.label}
              </text>
            </g>
          ))}
        </g>

        {/* Activity Bars and Labels */}
        <g transform={`translate(${SIDE_PADDING}, ${TOP_PADDING})`}>
          {chartActivities.map((act, index) => {
            const yPos = index * (BAR_HEIGHT + ROW_GAP);
            const barX = LABEL_WIDTH + dateToX(act.es);
            let barWidth = (Math.max(0, act.duration)) * DAY_WIDTH; // Duration 0 is a milestone
            if (act.duration === 0 && act.es) barWidth = DAY_WIDTH / 2; // Milestone width

            const progressWidth = barWidth * ((act.percentComplete || 0) / 100);
            
            let baselineBarX = 0, baselineBarWidth = 0;
            const baselineAct = baselineActivities.find(bAct => bAct.id === act.id);
            if (baselineAct && baselineAct.es) {
                baselineBarX = LABEL_WIDTH + dateToX(baselineAct.es);
                baselineBarWidth = (Math.max(0, baselineAct.duration)) * DAY_WIDTH;
                if (baselineAct.duration === 0) baselineBarWidth = DAY_WIDTH / 2;
            }

            return (
              <g key={act.id} transform={`translate(0, ${yPos})`}>
                <text x={LABEL_WIDTH - 8} y={BAR_HEIGHT / 2 + 4} textAnchor="end" fontSize="0.7rem" fill="#333" className="truncate">
                  <title>{act.name} (ID: {act.id.slice(0,6)}...)</title>
                  {act.name.length > (LABEL_WIDTH/7) ? act.name.substring(0,(LABEL_WIDTH/7)-3) + "..." : act.name}
                </text>
                
                {/* Baseline Bar (if selected and exists) */}
                {baselineAct && baselineBarWidth > 0 && (
                    <rect
                        x={baselineBarX}
                        y={(BAR_HEIGHT - BASELINE_BAR_HEIGHT) / 2 + BAR_HEIGHT * 0.6} // Position below main bar
                        width={baselineBarWidth -1}
                        height={BASELINE_BAR_HEIGHT}
                        fill="rgba(160, 160, 160, 0.7)" // Grey for baseline
                        stroke="rgba(100, 100, 100, 0.8)"
                        strokeWidth="0.5"
                        rx="2" ry="2"
                    >
                        <title>{`Línea Base: ${baselineAct.name}\nInicio: ${baselineAct.es}\nFin: ${baselineAct.ef}\nDuración: ${baselineAct.duration}d`}</title>
                    </rect>
                )}

                {/* Main Activity Bar (Planned/Scheduled) */}
                <rect
                  x={barX}
                  y="0"
                  width={barWidth -1 } 
                  height={BAR_HEIGHT}
                  fill={act.isCritical ? "rgba(239, 68, 68, 0.6)" : "rgba(59, 130, 246, 0.6)"} 
                  stroke={act.isCritical ? "rgba(185, 28, 28, 0.8)" : "rgba(37, 99, 235, 0.8)"}
                  strokeWidth="1"
                  rx="3" ry="3"
                >
                  <title>{`${act.name}\nInicio Plan.: ${act.es}\nFin Plan.: ${act.ef}\nDuración: ${act.duration}d\n%Comp: ${act.percentComplete || 0}%\nInicio Real: ${act.actualStartDate || '-'}\nFin Real: ${act.actualFinishDate || '-'}`}</title>
                </rect>

                {/* Progress Bar Overlay */}
                {progressWidth > 0 && (
                    <rect
                        x={barX}
                        y={(BAR_HEIGHT - PROGRESS_BAR_HEIGHT) / 2}
                        width={progressWidth -1}
                        height={PROGRESS_BAR_HEIGHT}
                        fill="url(#progressGradient)"
                        rx="2" ry="2"
                        style={{pointerEvents: 'none'}}
                    />
                )}
                
                {/* Actual Dates Markers (if exist and different from planned) */}
                {act.actualStartDate && act.actualStartDate !== act.es && (
                    <path d={`M ${LABEL_WIDTH + dateToX(act.actualStartDate)} -2 L ${LABEL_WIDTH + dateToX(act.actualStartDate)} ${BAR_HEIGHT+2}`} stroke="green" strokeWidth="1.5" strokeDasharray="3,2">
                         <title>Inicio Real: {act.actualStartDate}</title>
                    </path>
                )}
                {act.actualFinishDate && act.actualFinishDate !== act.ef && (
                     <path d={`M ${LABEL_WIDTH + dateToX(act.actualFinishDate)} -2 L ${LABEL_WIDTH + dateToX(act.actualFinishDate)} ${BAR_HEIGHT+2}`} stroke="darkgreen" strokeWidth="1.5" strokeDasharray="3,2">
                        <title>Fin Real: {act.actualFinishDate}</title>
                    </path>
                )}

                {barWidth > 50 && (
                    <text x={barX + 5} y={BAR_HEIGHT / 2 + 4} fontSize="0.6rem" fill={act.isCritical ? "#fff" : "#fff"} className="pointer-events-none">
                        {act.id.slice(0,5)}...
                    </text>
                )}
              </g>
            );
          })}
        </g>
      </svg>
    </div>
  );
};


// --- Scheduling View ---
const SchedulingView = () => {
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setAppNotification } = useContext(AppContext);
  const [scheduledActivities, setScheduledActivities] = useState([]);
  const [isCalculating, setIsCalculating] = useState(false);
  const [selectedBaselineForGantt, setSelectedBaselineForGantt] = useState('');


  useEffect(() => {
    if (selectedProject && selectedProject.activities) {
      setScheduledActivities(selectedProject.activities.sort((a,b) => (a.es && b.es) ? (dateToEpochDays(a.es) - dateToEpochDays(b.es)) : (a.id > b.id ? 1 : -1) ));
    }
  }, [selectedProject]);

  const handleCalculateSchedule = async () => {
    if (!selectedProject || !selectedProject.activities || !selectedProject.startDate) { 
      setAppNotification("error", "Datos del proyecto (actividades, fecha de inicio) incompletos para calcular cronograma."); 
      return; 
    }
    setIsCalculating(true); setIsLoading(true); 
    
    let activities = JSON.parse(JSON.stringify(selectedProject.activities || [])); 
    const projectStartDate = selectedProject.dataDate || selectedProject.startDate;

    // Initialize/Reset schedule fields
    activities.forEach(act => {
      act.es = null; act.ef = null; act.ls = null; act.lf = null; act.float = null; act.isCritical = false;
      act.duration = Number(act.duration) || 0; if (act.duration < 0) act.duration = 0; 
      act.predecessors = act.predecessors || [];
      // Respect actual dates if present and percentComplete > 0
      if (act.actualStartDate && (act.percentComplete || 0) > 0) {
          act.es = act.actualStartDate;
          if (act.duration > 0) {
              act.ef = addDaysToDate(act.es, Math.max(0, act.duration -1)); // Tentative EF based on original duration
          } else {
              act.ef = act.es; // Milestone
          }
          // If 100% complete, EF is actualFinishDate
          if ((act.percentComplete || 0) === 100 && act.actualFinishDate) {
              act.ef = act.actualFinishDate;
              // Recalculate duration based on actuals if both are set
              if (act.actualStartDate && act.actualFinishDate) {
                  act.duration = dateDiffInDays(act.actualStartDate, act.actualFinishDate) + 1;
              }
          }
      }
    });

    let changedInIteration, iterations = 0, MAX_ITERATIONS = activities.length * 2 + 5; 
    // Forward Pass (CPM)
    do {
        changedInIteration = false; iterations++;
        activities.forEach(act => {
            // Skip if already started and not finished (ES/EF fixed by actuals)
            if (act.actualStartDate && (act.percentComplete || 0) > 0 && (act.percentComplete || 0) < 100) {
                // ES/EF are already set based on actualStartDate and duration.
                // No change from predecessors for these.
                return;
            }
            // If 100% complete, ES/EF are fixed by actuals
            if ((act.percentComplete || 0) === 100 && act.actualStartDate && act.actualFinishDate) {
                if (act.es !== act.actualStartDate) { act.es = act.actualStartDate; changedInIteration = true;}
                if (act.ef !== act.actualFinishDate) { act.ef = act.actualFinishDate; changedInIteration = true;}
                return;
            }

            let newES;
            if (act.predecessors.length === 0) {
                newES = projectStartDate; // Default start for activities without predecessors
            } else {
                const predecessorEFs = act.predecessors.map(pId => {
                    const pred = activities.find(p => p.id === pId);
                    return pred ? pred.ef : null; // Get EF of predecessor
                }).filter(Boolean); // Filter out nulls (if a predecessor isn't found or doesn't have EF yet)
                
                if (predecessorEFs.length === act.predecessors.length && predecessorEFs.length > 0) { // All predecessors have EFs
                    newES = addDaysToDate(maxDate(predecessorEFs), 1); // Start day after latest predecessor finishes
                } else {
                    newES = act.es; // Keep current ES if not all predecessors are ready
                }
            }
            
            if (newES && newES !== act.es) { act.es = newES; changedInIteration = true; }
            if (act.es) { 
                const newEF = addDaysToDate(act.es, Math.max(0, act.duration -1)); 
                if (newEF !== act.ef) { act.ef = newEF; changedInIteration = true; } 
            }
        });
    } while (changedInIteration && iterations < MAX_ITERATIONS);
    if (iterations >= MAX_ITERATIONS) console.warn("Max iterations reached in Forward Pass. Schedule might be unstable due to circular dependencies or very long chains.");
    
    const projectFinishDate = maxDate(activities.map(act => act.ef).filter(Boolean)) || projectStartDate;
    iterations = 0; 
    // Backward Pass (CPM)
    do {
        changedInIteration = false; iterations++;
        [...activities].reverse().forEach(act => { // Iterate backwards
            // Skip if 100% complete (LS/LF fixed by actuals)
            if ((act.percentComplete || 0) === 100 && act.actualStartDate && act.actualFinishDate) {
                if (act.ls !== act.actualStartDate) {act.ls = act.actualStartDate; changedInIteration = true;}
                if (act.lf !== act.actualFinishDate) {act.lf = act.actualFinishDate; changedInIteration = true;}
                return;
            }

            const successors = activities.filter(succ => succ.predecessors.includes(act.id));
            let newLF;
            if (successors.length === 0) {
                newLF = act.ef || projectFinishDate; // If no successors, LF is its own EF or project finish
            } else {
                const successorLSs = successors.map(s => s.ls).filter(Boolean);
                if (successorLSs.length === successors.length && successorLSs.length > 0) { // All successors have LSs
                    newLF = addDaysToDate(minDate(successorLSs), -1); // Finish day before earliest successor starts
                } else {
                    newLF = act.lf; // Keep current LF if not all successors are ready
                }
            }

            if (newLF && newLF !== act.lf) { act.lf = newLF; changedInIteration = true; }
            if (act.lf) { 
                const newLS = addDaysToDate(act.lf, -(Math.max(0, act.duration - 1))); 
                if (newLS !== act.ls) { act.ls = newLS; changedInIteration = true; } 
            }
        });
    } while (changedInIteration && iterations < MAX_ITERATIONS);
    if (iterations >= MAX_ITERATIONS) console.warn("Max iterations reached in Backward Pass.");

    let minFloat = Infinity;
    activities.forEach(act => {
      if (act.ls && act.es) { 
          act.float = dateDiffInDays(act.es, act.ls); 
          if (act.float < minFloat) minFloat = act.float; 
      } else {
          act.float = null; 
      }
    });
    activities.forEach(act => { act.isCritical = act.float !== null && act.float <= (minFloat + 0.01); }); // Allow for small float discrepancies
    
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    try {
      await updateDoc(projectDocRef, { activities: activities });
      setScheduledActivities(activities.sort((a,b) => (a.es && b.es) ? (dateToEpochDays(a.es) - dateToEpochDays(b.es)) : (a.id > b.id ? 1 : -1)));
      setAppNotification("success", "Cronograma calculado y guardado exitosamente.");
    } catch (e) { console.error("Error guardando cronograma:", e); setAppNotification("error", "Error al guardar el cronograma calculado."); }
    finally { setIsCalculating(false); setIsLoading(false); }
  };

  const getPredecessorDetails = (predIds) => {
    if (!predIds || predIds.length === 0) return 'Ninguna';
    return predIds.map(id => {
        const predAct = selectedProject?.activities?.find(act => act.id === id);
        return predAct ? `${predAct.id.slice(0,6)}... (${predAct.name.slice(0,10)}...)` : 'ID desc.';
    }).join(', ');
  };

  if (!selectedProject) return <LoadingSpinner message="Cargando datos de programación..." />;
  return (
    <div className="p-1 md:p-4">
      <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
        <h2 className="text-xl md:text-2xl font-semibold">Programación: {selectedProject.name}</h2>
        <button onClick={handleCalculateSchedule} disabled={isCalculating || !(selectedProject?.activities?.length > 0)}
          className="btn-primary px-3 py-1.5 md:px-4 md:py-2 text-sm flex items-center space-x-2 disabled:opacity-50">
          <Play size={18} /> <span>{isCalculating ? 'Calculando...' : 'Calcular Cronograma (CPM)'}</span>
        </button>
      </div>
      {isCalculating && <LoadingSpinner message="Calculando cronograma..." />}
      {!isCalculating && scheduledActivities.length === 0 && <Notification type="info" message="No hay actividades para programar. Añade actividades en la sección correspondiente." />}
      {!isCalculating && scheduledActivities.length > 0 && (
        <>
          <div className="overflow-x-auto shadow-md rounded-lg mb-6">
            <table className="min-w-full bg-white border text-xs">
              <thead className="bg-gray-100"><tr>{['ID', 'Nombre', 'Dur.', 'Predec.', 'ES', 'EF', 'LS', 'LF', 'Holgura', 'Crítica', '% Comp.'].map(h => <th key={h} className="th-style-xs whitespace-nowrap">{h}</th>)}</tr></thead>
              <tbody className="divide-y divide-gray-200">{scheduledActivities.map(act => <tr key={act.id} className={`hover:bg-gray-50 ${act.isCritical ? 'bg-red-50 font-medium' : ''} ${ (act.percentComplete || 0) === 100 ? 'bg-green-50' : ''}`}>
                <td className="td-style-xs font-mono" title={act.id}>{act.id.slice(0,6)}...</td><td className="td-style-xs">{act.name}</td>
                <td className="td-style-xs text-center">{act.duration}</td><td className="td-style-xs" title={getPredecessorDetails(act.predecessors)}>{(act.predecessors || []).length > 0 ? `${(act.predecessors || []).map(p => p.slice(0,6)+"...").join(', ')}` : '-'}</td>
                <td className="td-style-xs text-blue-700">{act.es||'-'}</td><td className="td-style-xs text-blue-700">{act.ef||'-'}</td>
                <td className="td-style-xs text-green-700">{act.ls||'-'}</td><td className="td-style-xs text-green-700">{act.lf||'-'}</td>
                <td className={`td-style-xs text-center ${act.float !== null && act.float <= 0 ? 'text-red-600 font-bold':'text-gray-600'}`}>{act.float !== null ? act.float : '-'}</td>
                <td className={`td-style-xs text-center font-semibold ${act.isCritical ? 'text-red-600':'text-gray-500'}`}>{act.isCritical?'Sí':'No'}</td>
                <td className="td-style-xs text-center">{act.percentComplete || 0}%</td>
              </tr>)}</tbody>
            </table>
          </div>
          
          <div className="my-4">
            <label htmlFor="baselineSelectGantt" className="lbl text-sm">Seleccionar Línea Base para Gantt:</label>
            <select 
                id="baselineSelectGantt" 
                value={selectedBaselineForGantt} 
                onChange={(e) => setSelectedBaselineForGantt(e.target.value)}
                className="input-style max-w-xs text-sm"
            >
                <option value="">Ninguna (Actual)</option>
                {(selectedProject.baselines || []).map(b => <option key={b.id} value={b.id}>{b.name} ({new Date(b.createdAt).toLocaleDateString()})</option>)}
            </select>
          </div>

          <BasicGanttChart 
            activities={scheduledActivities} 
            projectStartDate={selectedProject.dataDate || selectedProject.startDate} 
            baselines={selectedProject.baselines}
            selectedBaselineId={selectedBaselineForGantt}
          />

          <div className="mt-6 p-3 bg-gray-50 rounded-lg text-xs text-gray-700 print:hidden">
            <h4 className="font-semibold mb-1 flex items-center"><HelpCircle size={14} className="mr-1 text-blue-500"/>Notas sobre la Programación:</h4>
            <ul className="list-disc list-inside space-y-0.5 pl-4">
              <li>Duraciones en días calendario. Relaciones son Fin-a-Inicio (FS) con 0 días de decalaje (lag).</li>
              <li>ES: Inicio Temprano, EF: Fin Temprano, LS: Inicio Tardío, LF: Fin Tardío.</li>
              <li>Holgura Total: LS - ES. Actividades críticas tienen la menor holgura (usualmente {'<='} 0).</li>
              <li>Cálculo basado en el Método de la Ruta Crítica (CPM) simplificado.</li>
              <li>La "Data Date" (Fecha de Estado) del proyecto (ver Configuración del Proyecto) se usa como fecha de inicio para actividades sin predecesoras o para el proyecto en general si no hay actuals.</li>
              <li>El progreso (%, Fechas Reales) puede influir en el cálculo del cronograma.</li>
            </ul>
          </div>
        </>
      )}
    </div>
  );
};


// --- Costs View ---
const CostsView = () => {
    const { selectedProject, isLoading } = useContext(AppContext);

    if (isLoading) return <LoadingSpinner message="Cargando costos del proyecto..." />;
    if (!selectedProject) return <Notification type="info" message="Por favor, selecciona un proyecto para ver sus costos." />;
    
    const projectActivities = selectedProject.activities || [];

    const totals = projectActivities.reduce((acc, act) => {
        acc.budgetedLabor += act.budgetedLaborCost || 0;
        acc.budgetedMaterial += act.budgetedMaterialCost || 0;
        acc.budgetedNonLabor += act.budgetedNonLaborCost || 0;
        acc.budgetedResource += act.budgetedResourceCost || 0;
        acc.budgetedTotal += act.budgetedTotalCost || 0;
        // Add actuals later if needed
        return acc;
    }, { budgetedLabor: 0, budgetedMaterial: 0, budgetedNonLabor: 0, budgetedResource: 0, budgetedTotal: 0 });

    return (
        <div className="p-1 md:p-4">
            <h2 className="text-xl md:text-2xl font-semibold mb-5 text-gray-800 border-b pb-2">Costos del Proyecto: {selectedProject.name}</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg shadow">
                    <h3 className="text-md font-medium text-blue-700 mb-1">Costo Total Presupuestado</h3>
                    <p className="text-2xl font-bold text-blue-800">{formatCurrency(totals.budgetedTotal)}</p>
                </div>
                <div className="bg-indigo-50 p-4 rounded-lg shadow">
                    <h3 className="text-md font-medium text-indigo-700 mb-1">Costo Recursos Presup.</h3>
                    <p className="text-xl font-bold text-indigo-800">{formatCurrency(totals.budgetedResource)}</p>
                </div>
                 <div className="bg-purple-50 p-4 rounded-lg shadow">
                    <h3 className="text-md font-medium text-purple-700 mb-1">Costo Fijo Presup. (Labor+Mat+NoLabor)</h3>
                    <p className="text-xl font-bold text-purple-800">{formatCurrency(totals.budgetedLabor + totals.budgetedMaterial + totals.budgetedNonLabor)}</p>
                </div>
            </div>

            <h3 className="text-lg font-semibold text-gray-700 mb-3">Desglose de Costos Presupuestados por Actividad</h3>
            {projectActivities.length === 0 && <Notification type="info" message="No hay actividades con costos definidos en este proyecto." />}
            
            {projectActivities.length > 0 && (
                <div className="overflow-x-auto shadow-md rounded-lg">
                    <table className="min-w-full bg-white border text-sm">
                        <thead className="bg-gray-50">
                            <tr>
                                {['ID Act.', 'Nombre Act.', 'M. Obra Fija ($)', 'Materiales Fijos ($)', 'No M.Obra Fijos ($)', 'Recursos Asig. ($)', 'Total Presup. ($)'].map(h=><th key={h} className="th-style">{h}</th>)}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {projectActivities.map(act => (
                                <tr key={act.id} className="hover:bg-gray-50">
                                    <td className="td-style font-mono text-xs" title={act.id}>{act.id.slice(0,8)}...</td>
                                    <td className="td-style">{act.name}</td>
                                    <td className="td-style text-right">{formatCurrency(act.budgetedLaborCost)}</td>
                                    <td className="td-style text-right">{formatCurrency(act.budgetedMaterialCost)}</td>
                                    <td className="td-style text-right">{formatCurrency(act.budgetedNonLaborCost)}</td>
                                    <td className="td-style text-right">{formatCurrency(act.budgetedResourceCost)}</td>
                                    <td className="td-style font-semibold text-right">{formatCurrency(act.budgetedTotalCost)}</td>
                                </tr>
                            ))}
                        </tbody>
                        <tfoot className="bg-gray-100">
                            <tr>
                                <td colSpan="2" className="px-3 py-2 text-right font-bold">TOTAL PROYECTO:</td>
                                <td className="px-3 py-2 text-right font-bold">{formatCurrency(totals.budgetedLabor)}</td>
                                <td className="px-3 py-2 text-right font-bold">{formatCurrency(totals.budgetedMaterial)}</td>
                                <td className="px-3 py-2 text-right font-bold">{formatCurrency(totals.budgetedNonLabor)}</td>
                                <td className="px-3 py-2 text-right font-bold">{formatCurrency(totals.budgetedResource)}</td>
                                <td className="px-3 py-2 text-right font-extrabold text-base">{formatCurrency(totals.budgetedTotal)}</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            )}
            <div className="mt-6 p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg text-xs text-yellow-800 print:hidden">
                <h4 className="font-semibold mb-1">Funcionalidad Futura (Costos):</h4>
                <ul className="list-disc list-inside space-y-0.5">
                    <li>Registro y visualización de Costos Reales.</li>
                    <li>Comparación detallada Presupuesto vs. Real.</li>
                    <li>Indicadores básicos de Valor Ganado (EVM).</li>
                    <li>Curvas S de costos.</li>
                </ul>
            </div>
        </div>
    );
};

// --- Risk Editor Component ---
const RiskEditor = () => {
    const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setAppNotification, openConfirmationModal } = useContext(AppContext);
    const [risks, setRisks] = useState([]);
    const [showRiskModal, setShowRiskModal] = useState(false);
    const [currentRisk, setCurrentRisk] = useState(null);
    const initialRiskForm = { id: '', description: '', probability: 'Medium', impact: 'Medium', status: 'Open', responsePlan: '', owner: '' };
    const [riskFormData, setRiskFormData] = useState(initialRiskForm);

    const probabilityOptions = ['Very Low', 'Low', 'Medium', 'High', 'Very High'];
    const impactOptions = ['Very Low', 'Low', 'Medium', 'High', 'Very High'];
    const statusOptions = ['Open', 'In Progress', 'Closed', 'Rejected'];

    useEffect(() => {
        if (selectedProject && selectedProject.risks) {
            setRisks(selectedProject.risks);
        } else {
            setRisks([]);
        }
    }, [selectedProject]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setRiskFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleOpenModal = (risk = null) => {
        setCurrentRisk(risk);
        if (risk) {
            setRiskFormData({ ...initialRiskForm, ...risk });
        } else {
            setRiskFormData({ ...initialRiskForm, id: `risk-${crypto.randomUUID()}` });
        }
        setShowRiskModal(true);
    };

    const handleSaveRisk = async () => {
        if (!riskFormData.description.trim()) {
            setAppNotification("error", "La descripción del riesgo es obligatoria.");
            return;
        }
        // Further validation can be added here
        setIsLoading(true);
        const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
        let updatedRisks = currentRisk ? risks.map(r => r.id === currentRisk.id ? riskFormData : r) : [...risks, riskFormData];
        
        try {
            await updateDoc(projectDocRef, { risks: updatedRisks });
            setShowRiskModal(false); setCurrentRisk(null);
            setAppNotification("success", `Riesgo "${riskFormData.description.substring(0,30)}..." ${currentRisk ? 'actualizado' : 'añadido'}.`);
        } catch (e) {
            console.error("Error guardando riesgo:", e);
            setAppNotification("error", "Error al guardar el riesgo.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteRisk = (riskId, riskDescription) => {
        openConfirmationModal(
            `¿Estás seguro de que quieres eliminar el riesgo "${riskDescription.substring(0,50)}..." (ID: ...${riskId.slice(-6)})?`,
            async () => {
                setIsLoading(true);
                const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
                const remainingRisks = risks.filter(r => r.id !== riskId);
                try {
                    await updateDoc(projectDocRef, { risks: remainingRisks });
                    setAppNotification("success", `Riesgo eliminado.`);
                } catch (e) {
                    console.error("Error eliminando riesgo:", e);
                    setAppNotification("error", "Error al eliminar el riesgo.");
                } finally {
                    setIsLoading(false);
                }
            }
        );
    };
    
    if (!selectedProject) return <LoadingSpinner message="Cargando riesgos..." />;

    return (
        <div className="p-1 md:p-4">
            <div className="flex justify-between items-center mb-5 pb-2 border-b">
                <h2 className="text-xl md:text-2xl font-semibold">Gestión de Riesgos: {selectedProject.name}</h2>
                <button onClick={() => handleOpenModal()} className="btn-primary px-4 py-2 text-sm flex items-center space-x-2">
                    <PlusCircle size={18} /> <span>Añadir Riesgo</span>
                </button>
            </div>
            {risks.length === 0 && <Notification type="info" message="No hay riesgos identificados para este proyecto." />}
            {risks.length > 0 && (
                 <div className="overflow-x-auto shadow-md rounded-lg">
                    <table className="min-w-full bg-white border text-sm">
                        <thead className="bg-gray-50">
                            <tr>{['ID', 'Descripción', 'Probabilidad', 'Impacto', 'Estado', 'Responsable', 'Acciones'].map(h => <th key={h} className="th-style">{h}</th>)}</tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {risks.map(risk => (
                                <tr key={risk.id} className="hover:bg-gray-50">
                                    <td className="td-style font-mono text-xs" title={risk.id}>{risk.id.slice(0,8)}...</td>
                                    <td className="td-style whitespace-normal max-w-xs">{risk.description}</td>
                                    <td className="td-style">{risk.probability}</td>
                                    <td className="td-style">{risk.impact}</td>
                                    <td className="td-style">{risk.status}</td>
                                    <td className="td-style">{risk.owner || '-'}</td>
                                    <td className="td-style space-x-1.5">
                                        <button onClick={() => handleOpenModal(risk)} title="Editar Riesgo" className="btn-icon text-blue-600"><Edit2 size={17}/></button>
                                        <button onClick={() => handleDeleteRisk(risk.id, risk.description)} title="Eliminar Riesgo" className="btn-icon text-red-600"><Trash2 size={17}/></button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {showRiskModal && (
                 <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50">
                    <div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-xl">
                        <h3 className="text-lg md:text-xl font-semibold mb-4">{currentRisk ? 'Editar' : 'Añadir'} Riesgo</h3>
                        <form onSubmit={(e) => { e.preventDefault(); handleSaveRisk(); }} className="space-y-4">
                            <div><label htmlFor="riskDescription" className="lbl">Descripción del Riesgo</label><textarea name="description" id="riskDescription" value={riskFormData.description} onChange={handleInputChange} className="w-full input-style min-h-[80px]" required /></div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div><label htmlFor="riskProbability" className="lbl">Probabilidad</label><select name="probability" id="riskProbability" value={riskFormData.probability} onChange={handleInputChange} className="w-full input-style">{probabilityOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}</select></div>
                                <div><label htmlFor="riskImpact" className="lbl">Impacto</label><select name="impact" id="riskImpact" value={riskFormData.impact} onChange={handleInputChange} className="w-full input-style">{impactOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}</select></div>
                                <div><label htmlFor="riskStatus" className="lbl">Estado</label><select name="status" id="riskStatus" value={riskFormData.status} onChange={handleInputChange} className="w-full input-style">{statusOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}</select></div>
                                <div><label htmlFor="riskOwner" className="lbl">Responsable (Opcional)</label><input type="text" name="owner" id="riskOwner" value={riskFormData.owner} onChange={handleInputChange} className="w-full input-style" /></div>
                            </div>
                            <div><label htmlFor="riskResponsePlan" className="lbl">Plan de Respuesta (Opcional)</label><textarea name="responsePlan" id="riskResponsePlan" value={riskFormData.responsePlan} onChange={handleInputChange} className="w-full input-style min-h-[60px]" /></div>
                            <div className="flex justify-end space-x-3 pt-3">
                                <button type="button" onClick={() => setShowRiskModal(false)} className="btn-secondary px-4 py-2 text-sm">Cancelar</button>
                                <button type="submit" className="btn-primary px-4 py-2 text-sm">{currentRisk ? 'Guardar Cambios' : 'Añadir Riesgo'}</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

// --- Baseline Manager Component ---
const BaselineManager = () => {
    const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setAppNotification, openConfirmationModal } = useContext(AppContext);
    const [baselines, setBaselines] = useState([]);
    const [baselineName, setBaselineName] = useState('');

    useEffect(() => {
        if (selectedProject && selectedProject.baselines) {
            setBaselines(selectedProject.baselines.sort((a,b) => new Date(b.createdAt) - new Date(a.createdAt)));
        } else {
            setBaselines([]);
        }
    }, [selectedProject]);

    const handleCreateBaseline = async () => {
        if (!baselineName.trim()) {
            setAppNotification("error", "El nombre de la línea base es obligatorio.");
            return;
        }
        if (!selectedProject || !selectedProject.activities) {
            setAppNotification("error", "No hay datos de proyecto o actividades para crear una línea base.");
            return;
        }
        setIsLoading(true);
        const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
        
        // Deep copy activities to avoid modifying the original live data via reference
        const activitiesSnapshot = JSON.parse(JSON.stringify(selectedProject.activities));

        const newBaseline = {
            id: `base-${crypto.randomUUID()}`,
            name: baselineName,
            createdAt: new Date().toISOString(),
            dataDate: selectedProject.dataDate || selectedProject.startDate, // Capture current data date
            activitiesSnapshot: activitiesSnapshot, // Store a snapshot of current activities
        };
        const updatedBaselines = [...(selectedProject.baselines || []), newBaseline];

        try {
            await updateDoc(projectDocRef, { baselines: updatedBaselines });
            setBaselineName(''); // Reset name field
            setAppNotification("success", `Línea base "${baselineName}" creada exitosamente.`);
        } catch (e) {
            console.error("Error creando línea base:", e);
            setAppNotification("error", "Error al crear la línea base.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteBaseline = (baselineId, name) => {
        openConfirmationModal(
            `¿Estás seguro de que quieres eliminar la línea base "${name}"? Esta acción es irreversible.`,
            async () => {
                setIsLoading(true);
                const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
                const remainingBaselines = (selectedProject.baselines || []).filter(b => b.id !== baselineId);
                try {
                    await updateDoc(projectDocRef, { baselines: remainingBaselines });
                    setAppNotification("success", `Línea base "${name}" eliminada.`);
                } catch (e) {
                    console.error("Error eliminando línea base:", e);
                    setAppNotification("error", "Error al eliminar la línea base.");
                } finally {
                    setIsLoading(false);
                }
            }
        );
    };
    
    if (!selectedProject) return <LoadingSpinner message="Cargando líneas base..." />;

    return (
        <div className="p-1 md:p-4">
            <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
                <h2 className="text-xl md:text-2xl font-semibold">Líneas Base del Proyecto: {selectedProject.name}</h2>
            </div>

            <div className="mb-6 p-4 bg-gray-50 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-700 mb-2">Crear Nueva Línea Base</h3>
                <div className="flex flex-col sm:flex-row sm:items-end gap-3">
                    <div className="flex-grow">
                        <label htmlFor="baselineName" className="lbl">Nombre de la Línea Base</label>
                        <input 
                            type="text" 
                            id="baselineName" 
                            value={baselineName} 
                            onChange={(e) => setBaselineName(e.target.value)} 
                            className="w-full input-style" 
                            placeholder="Ej: Línea Base Inicial, Fin de Fase 1"
                        />
                    </div>
                    <button 
                        onClick={handleCreateBaseline} 
                        className="btn-primary px-4 py-2 text-sm flex items-center space-x-2 self-start sm:self-end h-10"
                        disabled={!baselineName.trim()}
                    >
                        <Save size={18} /> <span>Guardar Línea Base</span>
                    </button>
                </div>
                 <p className="text-xs text-gray-500 mt-2">Se guardará una copia del estado actual del cronograma (actividades, fechas, costos) como referencia.</p>
            </div>

            <h3 className="text-lg font-semibold text-gray-700 mb-3">Líneas Base Existentes</h3>
            {baselines.length === 0 && <Notification type="info" message="No hay líneas base guardadas para este proyecto." />}
            {baselines.length > 0 && (
                 <div className="overflow-x-auto shadow-md rounded-lg">
                    <table className="min-w-full bg-white border text-sm">
                        <thead className="bg-gray-50">
                            <tr>{['Nombre', 'Fecha Creación', 'Data Date Capturada', 'Nº Actividades', 'Acciones'].map(h => <th key={h} className="th-style">{h}</th>)}</tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {baselines.map(b => (
                                <tr key={b.id} className="hover:bg-gray-50">
                                    <td className="td-style font-semibold">{b.name}</td>
                                    <td className="td-style">{new Date(b.createdAt).toLocaleString()}</td>
                                    <td className="td-style">{b.dataDate ? new Date(b.dataDate + 'T00:00:00Z').toLocaleDateString() : '-'}</td>
                                    <td className="td-style text-center">{(b.activitiesSnapshot || []).length}</td>
                                    <td className="td-style space-x-1.5">
                                        {/* <button title="Ver Detalles (Próximamente)" className="btn-icon text-blue-600 opacity-50 cursor-not-allowed"><Eye size={17}/></button> */}
                                        <button onClick={() => handleDeleteBaseline(b.id, b.name)} title="Eliminar Línea Base" className="btn-icon text-red-600"><Trash2 size={17}/></button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

// --- Progress Tracking View (Placeholder, can be expanded) ---
const ProgressTrackingView = () => {
    const { selectedProject, setCurrentView, setAppNotification } = useContext(AppContext); // Added setCurrentView

    if (!selectedProject) return <LoadingSpinner message="Cargando datos de avance..." />;
    
    const activitiesWithProgress = (selectedProject.activities || []).filter(act => act.percentComplete > 0 || act.actualStartDate);
    const overallProgress = selectedProject.activities?.length > 0 ? 
        (selectedProject.activities.reduce((sum, act) => sum + (act.percentComplete || 0), 0) / selectedProject.activities.length).toFixed(1) : 0;

    return (
        <div className="p-1 md:p-4">
            <h2 className="text-xl md:text-2xl font-semibold mb-5 text-gray-800 border-b pb-2">Seguimiento de Avance: {selectedProject.name}</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="bg-green-50 p-4 rounded-lg shadow">
                    <h3 className="text-md font-medium text-green-700 mb-1">Progreso General Estimado</h3>
                    <p className="text-2xl font-bold text-green-800">{overallProgress}%</p>
                    <p className="text-xs text-gray-500">(Basado en % completado promedio de actividades)</p>
                </div>
                 <div className="bg-yellow-50 p-4 rounded-lg shadow">
                    <h3 className="text-md font-medium text-yellow-700 mb-1">Actividades con Avance</h3>
                    <p className="text-2xl font-bold text-yellow-800">{activitiesWithProgress.length} / {(selectedProject.activities || []).length}</p>
                </div>
            </div>

            <p className="text-gray-600 mb-4">
                El avance de las actividades se registra individualmente en la sección <button onClick={() => setCurrentView('activities')} className="text-blue-600 hover:underline font-medium">Actividades</button>.
                Allí puedes actualizar el "% Completado", las "Fechas de Inicio/Fin Reales".
            </p>
            <p className="text-gray-600 mb-4">
                La "Data Date" (Fecha de Estado) del proyecto, configurada en "Proyecto" -&gt; "Configuración", es crucial. Se usa como referencia para el cálculo del cronograma y para registrar el progreso si no se especifican fechas reales.
            </p>

            <h3 className="text-lg font-semibold text-gray-700 mb-3 mt-6">Resumen de Actividades con Avance</h3>
            {activitiesWithProgress.length === 0 && <Notification type="info" message="Ninguna actividad tiene progreso registrado aún." />}
            {activitiesWithProgress.length > 0 && (
                 <div className="overflow-x-auto shadow-md rounded-lg">
                    <table className="min-w-full bg-white border text-sm">
                        <thead className="bg-gray-50">
                            <tr>{['ID Act.', 'Nombre Act.', '% Comp.', 'Inicio Real', 'Fin Real', 'Dur. Orig.'].map(h => <th key={h} className="th-style">{h}</th>)}</tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {activitiesWithProgress.map(act => (
                                <tr key={act.id} className="hover:bg-gray-50">
                                    <td className="td-style font-mono text-xs" title={act.id}>{act.id.slice(0,8)}...</td>
                                    <td className="td-style">{act.name}</td>
                                    <td className="td-style text-center">{act.percentComplete || 0}%</td>
                                    <td className="td-style text-center">{act.actualStartDate || '-'}</td>
                                    <td className="td-style text-center">{act.actualFinishDate || '-'}</td>
                                    <td className="td-style text-center">{act.duration}d</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            <div className="mt-8 p-3 bg-sky-50 border-l-4 border-sky-400 rounded-lg text-xs text-sky-800 print:hidden">
                <h4 className="font-semibold mb-1">Funcionalidad Futura (Avance):</h4>
                <ul className="list-disc list-inside space-y-0.5">
                    <li>Cálculo de Duración Restante y Fechas de Fin Proyectadas.</li>
                    <li>Entrada de Horas Reales / Hojas de Tiempo (Timesheets).</li>
                    <li>Aplicar Reales (Apply Actuals) para actualizar el cronograma con el progreso.</li>
                    <li>Análisis de Valor Ganado (EVM) más detallado.</li>
                </ul>
            </div>
        </div>
    );
};


// --- Auxiliary Components ---
const LoadingSpinner = ({ message = "Cargando..." }) => (
  <div className="flex flex-col items-center justify-center h-full p-4 text-center">
    <svg className="animate-spin h-8 w-8 text-blue-500 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
    <p className="text-sm text-gray-600">{message}</p>
  </div>
);

const Notification = ({ type, message, onClose }) => {
  const typeClasses = { 
    error: { bg: 'bg-red-100', border: 'border-red-500', text: 'text-red-700', iconColor: 'text-red-500', Icon: AlertCircle }, 
    success: { bg: 'bg-green-100', border: 'border-green-500', text: 'text-green-700', iconColor: 'text-green-500', Icon: CheckCircle }, 
    info: { bg: 'bg-blue-100', border: 'border-blue-500', text: 'text-blue-700', iconColor: 'text-blue-500', Icon: Info },
    warning: { bg: 'bg-yellow-100', border: 'border-yellow-500', text: 'text-yellow-700', iconColor: 'text-yellow-500', Icon: AlertTriangle }
  };
  const currentType = typeClasses[type] || typeClasses.info;
  return (
    <div className={`border-l-4 ${currentType.border} ${currentType.bg} p-3 my-3 rounded-md shadow-sm print:hidden fixed top-4 right-4 max-w-sm z-[200]`} role="alert">
      <div className="flex">
        <div className="py-1"><currentType.Icon size={20} className={`${currentType.iconColor} mr-2`} /></div>
        <div><p className={`text-sm font-medium ${currentType.text}`}>{message}</p></div>
        {onClose && (
          <button onClick={onClose} className="ml-auto -mx-1.5 -my-1.5 bg-transparent rounded-lg focus:ring-2 focus:ring-gray-400 p-1.5 hover:bg-gray-200 inline-flex h-8 w-8">
            <span className="sr-only">Cerrar</span>
            <svg className="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg>
          </button>
        )}
      </div>
    </div>
  );
};

const PlaceholderView = ({ viewName }) => {
    const {selectedProject} = useContext(AppContext);
    const viewLabels = { resources: "Recursos", baselines: "Líneas Base", progress: "Avance", reports: "Informes", risks: "Riesgos", layouts: "Layouts" };
    return (<div className="p-1 md:p-4 text-center"><h2 className="text-xl md:text-2xl font-semibold mb-4">{viewLabels[viewName] || viewName}</h2><div className="flex flex-col items-center justify-center bg-gray-50 p-8 rounded-lg shadow min-h-[300px]"><Briefcase size={60} className="text-gray-300 mb-6" /><p className="text-lg text-gray-500">Funcionalidad de "{viewLabels[viewName] || viewName}" próximamente.</p><p className="text-sm text-gray-400 mt-2">Gracias por tu paciencia.</p>{selectedProject && <p className="mt-4 text-xs text-gray-400">Proyecto: {selectedProject.name}</p>}</div></div>);
};

const GlobalStylesInjector = () => {
  useEffect(() => {
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = `
      body { margin: 0; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
      .input-style { padding: 0.5rem 0.75rem; border: 1px solid #D1D5DB; border-radius: 0.375rem; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out; font-size: 0.875rem; }
      .input-style:focus { outline: none; border-color: #3B82F6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25); }
      .input-style-xs, .input-xs-ro { padding: 0.25rem 0.5rem; border: 1px solid #D1D5DB; border-radius: 0.25rem; font-size: 0.75rem; }
      .input-xs-ro { background-color: #F3F4F6; cursor: default; }
      .btn-primary { background-color: #2563EB; color: white; font-weight: 500; border-radius: 0.375rem; transition: background-color 0.15s ease-in-out; }
      .btn-primary:hover { background-color: #1D4ED8; } .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
      .btn-secondary { background-color: #E5E7EB; color: #374151; font-weight: 500; border-radius: 0.375rem; border: 1px solid #D1D5DB; transition: background-color 0.15s ease-in-out; }
      .btn-secondary:hover { background-color: #D1D5DB; }
      .btn-icon { padding: 0.25rem; border-radius: 0.25rem; } .btn-icon:hover { background-color: rgba(0,0,0,0.05); }
      .font-inter { font-family: 'Inter', sans-serif; }
      .lbl { display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.25rem; }
      .lbl-xs { display: block; font-size: 0.75rem; font-weight: 500; color: #4B5563; margin-bottom: 0.1rem; }
      .th-style { padding: 0.65rem 0.75rem; text-align: left; font-size: 0.75rem; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em; background-color: #F9FAFB; }
      .td-style { padding: 0.65rem 0.75rem; white-space: nowrap; color: #374151; }
      .th-style-xs { padding: 0.5rem 0.65rem; text-align: left; font-size: 0.7rem; font-weight: 600; color: #4B5563; text-transform: uppercase; letter-spacing: 0.05em; background-color: #F9FAFB;}
      .td-style-xs { padding: 0.5rem 0.65rem; white-space: nowrap; color: #374151; font-size: 0.75rem; }
      @media print { .print\\:hidden { display: none; } }
    `;
    document.head.appendChild(styleSheet);
    const interFontLink = document.createElement('link');
    interFontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap';
    interFontLink.rel = 'stylesheet';
    document.head.appendChild(interFontLink);
    return () => { 
      if (document.head.contains(styleSheet)) document.head.removeChild(styleSheet); 
      if (document.head.contains(interFontLink)) document.head.removeChild(interFontLink);
    };
  }, []);
  return null;
};

export default function MainApp() {
  return ( <> <GlobalStylesInjector /> <App /> </> );
}
